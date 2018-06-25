 def _resolve_generic(self, product_or_project, item_type, dependencies, overrides, output_dir, object_create_fn=None):

        def dependency_key(dependency):
            return '{}@{}'.format(dependency.name, dependency.organisation)

        pickle_file = os.path.join(output_dir,
            '{}_resolved.pkl'.format(item_type))

        # Update all dependencies with the default organisation if they
        # don't already have an organisation.
        for dependency in dependencies:
            if getattr(dependency, 'organisation', None) is None:
                dependency.organisation = self.default_organisation

        if self.no_network:
            print(colorama.Fore.YELLOW + '   WARNING: Skipping network dependency resolution, using existing artifacts')

            if not os.path.isfile(pickle_file):
                raise RuntimeError('No dependencies have yet been resolved, no network option cannot be used.')

            # Read the resolved dependencies from the pickle file.
            # Using a pickle file allows us to skip some steps that are
            # slow, like parsing through the output directory to find
            # artifacts
            resolved_dependencies = pickle.load(file(pickle_file, 'rb'))

            # Create dictionaries of the previously resolved and requested
            # dependencies.
            resolved_dependency_dict = {dependency_key(dependency): dependency for dependency in resolved_dependencies}
            requested_dependency_dict = {dependency_key(dependency): dependency for dependency in dependencies}

                for dependency in dependencies:
                override = RepositoryIvy.search_for_dependency_in_overrides(dependency, overrides)
                if override:
                    force_revision = True
                    if override.is_revision_override():
                        revision = override.get_revision_string()
                    elif override.is_local_override():
                        revision = 'local.+'
                        local_directories.add(os.path.join(
                            override.get_local_directory(), '_publish_local'))
                        # Call this function to possibly automatically
                        # do a build of this local dependency.
                        override._autobuild_local = \
                            do_local_dependency_build(product_or_project,
                                item_type, dependency.name,
                                override.get_local_directory())
                else:
                    force_revision = getattr(dependency, 'force_revision', False)

            # Double check that the dependencies requested actually were
            # previously resolved.
            for requested_dependency in requested_dependency_dict:
                if requested_dependency not in resolved_dependency_dict:
                    raise RuntimeError('Requested dependency {} {} has not yet been resolved, no network option cannot be used.'.format(
                        item_type, requested_dependency))

            # Filter the resolved dependencies loaded from the pickle
            # file to only include the dependencies that have been requested.
            # This handles the case where different direct dependencies were
            # initially resolved (i.e. dependencies may change based on
            # target or build configuration).
            # Note that the requested dependencies only include the direct
            # dependencies, so we just include all transitive dependencies.
            # There is currently no way to determine if any transitive
            # dependencies should also be filtered out... this would be a
            # much harder problem.
            resolved_dependencies = [dependency for dependency in resolved_dependencies
                # Keep the dependency if it was requested OR if it is a
                # transitive dependency.
                if dependency_key(dependency) in requested_dependency_dict or
                   dependency._transitive_dependency]

        else:

            pyivy_dependencies = {}
            local_directories = set()

            for dependency in dependencies:
                override = RepositoryIvy.search_for_dependency_in_overrides(dependency, overrides)

                organisation = getattr(dependency, 'organisation',
                    self.default_organisation)

                revision = getattr(dependency, 'requested_revision', None)

                configurations = getattr(dependency, 'configurations', None)

                transitive = getattr(dependency, 'transitive_dependency', False)

                if override:
                    force_revision = True
                    if override.is_revision_override():
                        revision = override.get_revision_string()
                    elif override.is_local_override():
                        revision = 'local.+'
                        local_directories.add(os.path.join(
                            override.get_local_directory(), '_publish_local'))
                        # Call this function to possibly automatically
                        # do a build of this local dependency.
                        override._autobuild_local = \
                            do_local_dependency_build(product_or_project,
                                item_type, dependency.name,
                                override.get_local_directory())
                else:
                    force_revision = getattr(dependency, 'force_revision', False)

                pyivy_dependency = pyivy.IvyDependency(
                    dependency.name, organisation, revision,
                    force_revision=force_revision)
                pyivy_dependency._override = override
                pyivy_dependency._configurations = configurations
                pyivy_dependency._transitive_dependency = transitive

                key = '{}@{}'.format(dependency.name, organisation)
                pyivy_dependencies[key] = pyivy_dependency

            resolved_dependencies = self._do_network_resolve(
                product_or_project, item_type, pyivy_dependencies.values(),
                output_dir, local_directories)

            # Special case.  We need to verify that we did not pick up any
            # transitive dependencies that we are also overriding.
            # If this is the case, we have to (unfortunately) redo the
            # resolve process to pick up these transitive dependencies
            # either with a fixed revision or a local path.
            redo_resolution = False
            for resolved_dependency in resolved_dependencies:
                key = '{}@{}'.format(resolved_dependency.name, resolved_dependency.organisation)

                if key not in pyivy_dependencies:

                    override = RepositoryIvy.search_for_dependency_in_overrides(resolved_dependency, overrides)

                    if override:
                        resolved_dependency.force_revision = True
                        resolved_dependency._transitive_dependency = True
                        if override.is_revision_override():
                            resolved_dependency.revision = override.get_revision_string()
                        elif override.is_local_override():
                            resolved_dependency.revision = 'local.+'
                            local_directories.add(os.path.join(
                                override.get_local_directory(), '_publish_local'))
                            # Call this function to possibly automatically
                            # do a build of this local dependency.
                            override._autobuild_local = \
                                do_local_dependency_build(product_or_project,
                                    item_type, resolved_dependency.name,
                                    override.get_local_directory())

                        resolved_dependency._override = override
                        pyivy_dependencies[key] = resolved_dependency
                        redo_resolution = True

            if redo_resolution:
                resolved_dependencies = self._do_network_resolve(
                    product_or_project, item_type, pyivy_dependencies.values(),
                    output_dir, local_directories)

            # Assign _override to overriden resolved dependencies.
            # Set the value of transitive_dependency attribute based on whether
            # this dependency was directly resolved.
            for resolved_dependency in resolved_dependencies:
                key = '{}@{}'.format(resolved_dependency.name, resolved_dependency.organisation)

                if key in pyivy_dependencies:
                    dependency = pyivy_dependencies[key]
                    resolved_dependency._override = getattr(dependency, '_override', None)
                    resolved_dependency._transitive_dependency = getattr(dependency, '_transitive_dependency', False)
                else:
                    resolved_dependency._override = None
                    resolved_dependency._transitive_dependency = True

        resolved_dependency_objects = []

        for resolved_dependency in resolved_dependencies:
            if self._dependency_is_ignored(product_or_project, resolved_dependency, item_type):
                continue

            self._print_resolved_dependency(resolved_dependency)

            if object_create_fn:
                # Use the artifacts that come from the pickle file we loaded.
                artifacts = None
                if self.no_network:
                    artifacts = deepcopy(resolved_dependency.artifacts)

                dependency_object = object_create_fn(product_or_project,
                                                     resolved_dependency,
                                                     self.no_network,
                                                     artifacts)

                # Save a list of resolved artifacts into the pickle file.
                if not self.no_network:
                    resolved_dependency.artifacts = deepcopy(dependency_object.artifacts)
            else:
                dependency_object = resolved_dependency

            resolved_dependency_objects.append(dependency_object)

        self._write_manifest_file(item_type, output_dir, resolved_dependency_objects)

        if not self.no_network:
            f = file(pickle_file, 'wb')
            pickle.dump(resolved_dependencies, f, -1)
            f.close()

        return resolved_dependency_objects
