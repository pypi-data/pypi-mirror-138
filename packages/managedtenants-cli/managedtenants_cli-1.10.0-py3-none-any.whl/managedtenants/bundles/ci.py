import os
import sys
from pathlib import Path

import urllib3
import yaml
from gitlab.exceptions import GitlabError
from sretoolbox.utils.logger import get_text_logger

from managedtenants.bundles.bundle_builder import BundleBuilder
from managedtenants.bundles.index_builder import IndexBuilder
from managedtenants.utils.git import ChangeDetector, get_short_hash
from managedtenants.utils.gitlab_client import GitLab
from managedtenants.utils.quay_api import QuayApi

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOG = get_text_logger("app")

GITLAB_URL = os.environ.get("GITLAB_SERVER")
GITLAB_TOKEN = os.environ.get("GITLAB_TOKEN")
GITLAB_PROJECT = os.environ.get("GITLAB_PROJECT")

DOCKER_CONF = os.environ.get("DOCKER_CONF")


def get_single_addon(addons_dir, addon_name):
    """
    :param addon_name: Name of Addon
    :return: The changed addon path
    """
    target_addon = None
    for addon in addons_dir.iterdir():
        if addon.name == addon_name:
            target_addon = addon
            break
    return target_addon


# TODO: remove this function once flow has been verified with condition on L688
# pylint: disable=R1710
def post_managed_tenants_mr_metadata(
    dry_run,
    addon,
    addon_env,
    version,
    index_image,
):
    """
    TODO
    :param dry_run:
    :param addon:
    :param addon_env:
    :param version:
    :param index_image:
    :return:
    """

    if dry_run:
        return None

    gl = GitLab(url=GITLAB_URL, token=GITLAB_TOKEN, project=GITLAB_PROJECT)
    version_name = f"{addon.name}-{version}"

    addon_metadata_path = f"addons/{addon.name}/metadata/{addon_env}/addon.yaml"

    if gl.mr_exists(title=version_name):
        LOG.info("MR with the same name already exists. Aborting MR creation.")
        return None

    main_branch = "main"
    branch = f"{addon.name}-{get_short_hash()}"
    LOG.info("Creating branch %s", branch)

    gl.create_branch(new_branch=branch, source_branch=main_branch)

    try:
        raw_file = gl.project.files.get(
            file_path=addon_metadata_path, ref=main_branch
        )
    except GitlabError:
        exit_with_error(
            f"File {addon_metadata_path} does not exist in the managed-tenants"
            " repository. Please create it."
        )

    addon_metadata = yaml.load(raw_file.decode(), Loader=yaml.CSafeLoader)

    addon_metadata["indexImage"] = index_image.url_digest

    content_metadata = yaml.dump(addon_metadata, Dumper=yaml.CSafeDumper)

    commit_message = f"Updating metadata for {version_name}:{addon_env}"
    gl.update_file(
        branch_name=branch,
        file_path=addon_metadata_path,
        commit_message=commit_message,
        content=content_metadata,
    )

    if not gl.project.repository_compare(from_=main_branch, to=branch)["diffs"]:
        gl.delete_branch(branch=branch)
        LOG.info(
            "No changes when compared to %s. Aborting MR creation.", main_branch
        )
        return None

    gitlab_data = {
        "source_branch": branch,
        "target_branch": main_branch,
        "title": version_name,
        "remove_source_branch": True,
        "labels": [],
    }

    LOG.info("Posting MR to Managed Tenants")
    if not dry_run:
        return gl.project.mergerequests.create(gitlab_data)


# pylint: disable=R1710
def post_managed_tenants_mr(
    dry_run,
    addon,
    addon_env,
    version,
    index_image,
):
    """
    TODO
    :param dry_run:
    :param addon:
    :param addon_env:
    :param version:
    :param index_image:
    :return:
    """

    if dry_run:
        return None

    gl = GitLab(url=GITLAB_URL, token=GITLAB_TOKEN, project=GITLAB_PROJECT)
    version_name = f"{addon.name}-{version}"
    addon_version = f"{addon.name}.v{version}"

    addon_image_set = {
        "name": addon_version,
        "indexImage": index_image.url_digest,
        "relatedImages": [],
    }

    config_path = f"addons/{addon.name}/main/config.yaml"

    try:
        with open(config_path, "r", encoding="utf-8") as stream:
            try:
                config = yaml.safe_load(stream)
                ocm_config = config.get("ocm", {})

                # Populate OCM data in ImageSet
                for key in ocm_config:

                    # Ensure that we're not allowing any other keys
                    if key in [
                        "addOnParameters",
                        "subOperators",
                        "addOnRequirements",
                    ]:
                        val = ocm_config.get(key, {})
                        if val:
                            addon_image_set[key] = val

            except IOError as e:
                LOG.error(f"failed to read config file for {addon.name}: {e}")
    except FileNotFoundError as e:
        LOG.info(f"No config file present: {e}")

    addon_image_sets_path = (
        f"addons/{addon.name}/addonimagesets/{addon_env}/{addon_version}.yaml"
    )

    if gl.mr_exists(title=version_name):
        LOG.info("MR with the same name already exists. Aborting MR creation.")
        return None

    main_branch = "main"
    branch = f"{addon.name}-{get_short_hash()}"
    LOG.info("Creating branch %s", branch)

    gl.create_branch(new_branch=branch, source_branch=main_branch)

    image_set_content = yaml.dump(addon_image_set, Dumper=yaml.CSafeDumper)

    # Check if ImageSet file does not already exist
    if not gl.file_exists(
        file_path=addon_image_sets_path, target_branch=main_branch
    ):
        commit_message = f"Creating AddonImageSet for {addon.name}"
        gl.create_file(
            branch_name=branch,
            file_path=addon_image_sets_path,
            commit_message=commit_message,
            content=image_set_content,
        )
    else:
        commit_message = f"Updating AddonImageSet for {addon.name}"
        gl.update_file(
            branch_name=branch,
            file_path=addon_image_sets_path,
            commit_message=commit_message,
            content=image_set_content,
        )

    if not gl.project.repository_compare(from_=main_branch, to=branch)["diffs"]:
        gl.delete_branch(branch=branch)
        LOG.info(
            "No changes when compared to %s. Aborting MR creation.", main_branch
        )
        return None

    gitlab_data = {
        "source_branch": branch,
        "target_branch": main_branch,
        "title": version_name,
        "remove_source_branch": True,
        "labels": [],
    }

    LOG.info("Posting MR to Managed Tenants")
    if not dry_run:
        return gl.project.mergerequests.create(gitlab_data)


def exit_with_error(msg):
    LOG.error(msg)
    sys.exit(1)


def get_addon_environments(addon):
    """
    Returns a list of all environments that the managed-tenants
    metadata PRs must be made to.

    :param addon:
    :return:
    """
    path = f"addons/{addon.name}/main/config.yaml"
    try:
        with open(path, "r", encoding="utf-8") as addon_config:
            config = yaml.safe_load(addon_config)
            environments = config.get("environments", ["stage"])
            for environment in environments:
                if environment == "production":
                    exit_with_error(
                        "Pull Requests can not be raised by CI to managed"
                        " tenants production metadata"
                    )
                if environment not in ["stage", "integration"]:
                    exit_with_error(
                        "Invalid environment specified in config file. Valid"
                        " values are stage or integration"
                    )
    except IOError:
        LOG.info(
            f"No valid config file found for {addon.name}. Defaulting to"
            " 'stage'"
        )
        environments = ["stage"]
    return environments


def build_and_push_addon_bundles(
    addon,
    dry_run,
    quay_api,
    bundle_docker_file_path,
):
    """
    Builds and pushes bundle images from the passed addon's directory.
    """
    bundle_builder = BundleBuilder(
        addon_dir=addon,
        dry_run=dry_run,
        quay_api=quay_api,
        docker_conf_path=DOCKER_CONF,
    )
    err = bundle_builder.validate_local_bundles()
    if err:
        exit_with_error(err)

    bundle_images = bundle_builder.build_push_bundle_images_with_deps(
        versions=None,
        hash_string=get_short_hash(),
        docker_file_path=bundle_docker_file_path,
    )
    latest_version = bundle_builder.get_latest_version()
    return (bundle_images, latest_version)


def create_index_image(addon, dry_run, quay_api, bundle_images):
    """
    Builds and pushes an index image from the passed bundle images.
    """

    index_image_builder = IndexBuilder(
        addon_dir=addon,
        dry_run=dry_run,
        quay_api=quay_api,
        docker_conf_path=DOCKER_CONF,
    )
    index_image = index_image_builder.build_push_index_image(
        bundle_images=bundle_images,
        hash_string=get_short_hash(),
    )
    return index_image


def mtbundles_main(args):
    """
    Entrypoint for anything related to managed-tenants-bundles.

    Validates, builds and pushes both bundle images and index images.
    """
    dry_run = args.dry_run
    quay_org = Path(f"quay.io/{args.quay_org}/")
    quay_api = QuayApi(org=quay_org)

    target_addons = get_target_addons(args)
    for addon in target_addons:
        index_image = f"{quay_org}/{addon.name}-index"
        bundle_image = f"{quay_org}/{addon.name}-bundle"
        LOG.info(f"Building {index_image} and {bundle_image}...")
        if not dry_run:
            LOG.info(f"Pushing {index_image} and {bundle_image}...")

        bundle_images, latest_version = build_and_push_addon_bundles(
            addon=addon,
            dry_run=dry_run,
            quay_api=quay_api,
            bundle_docker_file_path=Path("Dockerfile"),
        )
        index_image = create_index_image(
            addon=addon,
            dry_run=dry_run,
            quay_api=quay_api,
            bundle_images=bundle_images,
        )
        if not dry_run:
            LOG.info(f"Index image {index_image} pushed and ready for use")

        if not dry_run:
            environments = get_addon_environments(addon)
            for env in environments:
                if addon.name == "reference-addon":
                    post_managed_tenants_mr(
                        dry_run=dry_run,
                        addon=addon,
                        addon_env=env,
                        version=latest_version,
                        index_image=index_image,
                    )
                else:
                    post_managed_tenants_mr_metadata(
                        dry_run=dry_run,
                        addon=addon,
                        addon_env=env,
                        version=latest_version,
                        index_image=index_image,
                    )


def get_target_addons(args):
    """
    Returns a list of targeted addons. 3 use cases:
        1. single addon
        2. all addons that have a changed file (using git diff)
        3. all addons
    """
    addons_dir = Path(args.addons_dir)
    dry_run = args.dry_run

    if args.addon_name:
        addon = get_single_addon(addons_dir, args.addon_name)
        if not addon:
            exit_with_error(f"Invalid addon name provided: {args.build_addon}")
        LOG.info(f"Targeting single addon {addon.name}...")
        return [addon]

    # TODO: (sblaisdo) deprecate the changed_addons workflow once the tooling is
    # more stable, and supports concurrently building+deploying index/bundle
    # images.
    if args.only_changed:
        LOG.info("Targeting changed addons as reported by git...")
        return ChangeDetector(
            addons_dir=addons_dir, dry_run=dry_run
        ).get_changed_addons()

    LOG.info(f"Targeting all addons in {addons_dir}.")
    return list(addons_dir.iterdir())
