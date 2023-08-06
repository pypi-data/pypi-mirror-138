import pathlib
from pathlib import Path
from argparse import ArgumentParser
from typing import Set, List
from urllib.parse import urlparse
# Kubernetes seems to use yaml 1.1 (https://github.com/kubernetes/kubernetes/issues/34146)
# Should switch to ruamel.yaml if it switches to yaml 1.2 as explained here
# https://stackoverflow.com/questions/1773805/how-can-i-parse-a-yaml-file-in-python/38922434#38922434
import yaml
import os


def is_url(url):
    try:
        result = urlparse(url)
        return any([result.query, result.netloc, result.scheme])
    except ValueError:
        return False


def extract_kustomization_dependencies(kustomization: dict) -> Set[Path]:
    """
    Extracts the dependencies of a kustomization.yaml file.
    """
    overlay_dependencies = set()

    if 'resources' in kustomization:
        overlay_dependencies |= \
            set(Path(resource).resolve(strict=True) for resource in
                [resource for resource in kustomization['resources'] if not is_url(resource)])

    # TODO: Not sure if components can be imported from external urls,
    #  currently supporting only in resources, should check
    if 'components' in kustomization:
        overlay_dependencies |= \
            set(Path(component).resolve(strict=True) for component in kustomization['components'])

    if 'generators' in kustomization:
        overlay_dependencies |= \
            set(Path(component).resolve(strict=True) for component in kustomization['generators'])

    if 'crd' in kustomization:
        overlay_dependencies |= \
            set(Path(crd).resolve(strict=True) for crd in kustomization['crd'])

    if 'configMapGenerator' in kustomization:
        if isinstance(kustomization['configMapGenerator'], dict) and 'files' in kustomization['configMapGenerator']:
            overlay_dependencies |= \
                set(Path(file).resolve(strict=True) for file in kustomization['configMapGenerator']['files'])
        elif isinstance(kustomization['configMapGenerator'], list):
            for patch in kustomization['configMapGenerator']:
                if 'files' in patch:
                    overlay_dependencies |= \
                        set(Path(file).resolve(strict=True) for file in patch['files'])

    if 'secretGenerator' in kustomization:
        if isinstance(kustomization['secretGenerator'], dict) and 'files' in kustomization['secretGenerator']:
            overlay_dependencies |= \
                set(Path(file).resolve(strict=True) for file in kustomization['secretGenerator']['files'])
        elif isinstance(kustomization['secretGenerator'], list):
            for patch in kustomization['secretGenerator']:
                if 'files' in patch:
                    overlay_dependencies |= \
                        set(Path(file).resolve(strict=True) for file in patch['files'])

    if 'openapi' in kustomization and 'path' in kustomization['openapi']:
        overlay_dependencies.add(Path(kustomization['openapi']['path']).resolve(strict=True))

    if 'patches' in kustomization:
        for patch in kustomization['patches']:
            if 'path' in patch:
                overlay_dependencies.add(Path(patch['path']).resolve(strict=True))

    if 'patchesJson6902' in kustomization:
        for patch in kustomization['patchesJson6902']:
            if 'path' in patch:
                overlay_dependencies.add(Path(patch['path']).resolve(strict=True))

    if 'patchesStrategicMerge' in kustomization:
        overlay_dependencies |= \
            set(Path(crd).resolve(strict=True) for crd in kustomization['patchesStrategicMerge'])

    if 'replacements' in kustomization:
        for patch in kustomization['replacements']:
            if 'path' in patch:
                overlay_dependencies.add(Path(patch['path']).resolve(strict=True))

    return overlay_dependencies


def get_overlay_dependencies(overlay: Path) -> Set[Path]:
    """
    Recursively extracts the dependencies of an overlay including it's sub overlays.
    """
    with open(str(overlay), 'r') as _file:
        try:
            kustomization = yaml.safe_load(_file)
        except yaml.YAMLError as exception:
            raise ValueError(f'Problem with overlay {overlay}') from exception

    # Change working directory to the path to the overlay
    # so that we could resolve the absolute path of it's dependencies
    previous_cwd = pathlib.Path.cwd()
    os.chdir(str(overlay.parent))

    overlay_dependencies = extract_kustomization_dependencies(kustomization)
    sub_dependencies = set()

    for sub_overlay in (dependency for dependency in overlay_dependencies if dependency.is_dir()):
        sub_dependencies |= get_overlay_dependencies(sub_overlay / 'kustomization.yaml')

    # Can't change set during iteration
    overlay_dependencies |= sub_dependencies

    # Add self as well, necessary in base overlay as it is dependent on itself
    overlay_dependencies.add(overlay)

    # Return old cwd
    os.chdir(previous_cwd)

    return overlay_dependencies


def get_changed_overlays(changed_files: Set[Path], base_overlays: Set[Path]) -> Set[Path]:
    changed_overlays = set()

    for overlay in base_overlays:
        if [overlay_dependency for overlay_dependency in get_overlay_dependencies(overlay)
           if overlay_dependency in changed_files]:
            changed_overlays.add(overlay)

    return changed_overlays


def main():
    parser = ArgumentParser()
    parser.add_argument('--changed-files', nargs='+', dest='changed_files',
                        help='The files that were changed', required=True)
    parser.add_argument('--base-overlays', nargs='+', dest='base_overlays',
                        help='The base overlays potentially affected', required=True)
    parser.add_argument('-o', '--output-file', dest='output_file',
                        help='The output file path', required=False)

    args = parser.parse_args()

    # Cast relative paths to absolute paths
    changed_files = set()
    base_overlays = set()

    for file_path in args.changed_files:
        changed_files.add(Path(file_path).resolve(strict=True))

    for overlay_path in args.base_overlays:
        base_overlays.add(Path(overlay_path).resolve(strict=True))

    print(' '.join(str(overlay) for overlay in get_changed_overlays(changed_files, base_overlays)),
          file=open(args.output_file, 'w') if args.output_file else None)


if __name__ == '__main__':
    main()
