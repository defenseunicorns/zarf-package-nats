#!/usr/bin/env python
import asyncio
import io
import os
import sys
import nats
import yaml

servers = os.environ.get("NATS_URL", "nats://localhost:4222").split(",")
bucket_name = "sections"


def get_hull_sections(hull_number, state_index_yaml):
    for hull in state_index_yaml['hulls']:
        if hull['id'] == hull_number:
            return hull['sections']
    return None  # Return None if not found


def get_revision(hull_number, section_number, state_index_yaml):
    for hull in state_index_yaml['hulls']:
        if hull['id'] == hull_number:
            for section in hull['sections']:
                if section['id'] == section_number:
                    return section['revision']
    return None  # Return None if no revision is found


async def main(hull_number):
    # Connect to NATS and
    nats_client = await nats.connect(servers)
    jetstream_context = nats_client.jetstream()
    object_store = await jetstream_context.object_store(bucket_name)
    object_result = await object_store.get("state_index.yaml")
    state_index_yaml = yaml.safe_load(io.BytesIO(object_result.data))

    # Loop through each section
    for section in get_hull_sections(hull_number, state_index_yaml):
        # Get the correct revision
        revision = get_revision(hull_number, section["id"], state_index_yaml)

        # Download the file to the CWD

    # # Loop through each section
    # for section in range(1, 4):
    #     # Get the latest revision
    #     revision = get_latest_revision(hull_number, section)
    #     file_name = f"section_{section}_rev_{revision}.blob"
    #
    #     # Download the blob file
    #     download_blob_from_nats(bucket_name, file_name)

    print("All required .blob files have been downloaded.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python download_blobs.py <hull_number>")
        sys.exit(1)

    input_hull_number = sys.argv[1]
    asyncio.run(main(input_hull_number))
