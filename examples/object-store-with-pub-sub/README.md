# Example: Object Storage with PubSub

## Scenario

We are setting up an example environment where we have a fictional shipyard that is building spaceships. They are building Enterprise-class ships, with the first ships being NCC-1701 (USS Enterprise) followed by NCC-1702 (USS Farragut). The shipyard is using computer-aided design (CAD) to build the ship, and they are publishing their design data to us so that we may use it when maintaining the ship.

Ships are big, and it would be too hard to design and build the whole ship at once. So, the shipyard has created a concept where the ship is broken down into Sections. The real ship has thousands of Sections, but for simplicity's sake, we will assume the ship has just 3 Sections.

Whenever a change is made to a Section, a new Revision is created and distributed to us. Revisions are distributed to us as binary blobs (file extension `.blob`).

To consume the data, I need to retrieve the binary blob for each section of the ship, making sure to pick the right revision according to the advertised current state of the ship. 

### Objectives

- Create a historical "database" of Revisions, which will be added to whenever a new Revision is published
- Provide the current state of the ships

    > | Hull | Section | Revision |
    > |------|---------|----------|
    > | 1701 | 1       | A        |
    > | 1701 | 2       | A        |
    > | 1701 | 3       | A        |
    > | 1702 | 1       | A        |
    > | 1702 | 2       | A        |
    > | 1702 | 3       | B        |
    >
    > In this example, we have 2 ships with 3 sections each. Hull 1701 (the Enterprise) was designed and built using Revision A of all 3 sections. Hull 1702 (the Farragut) uses Revision A of Sections 1 and 2, but the shipyard made a change to Section 3 when designing Hull 1702, so 1702 uses Revision B of Section 3. We would therefore expect 4 entries in the Revision Database: `section_1_rev_a.blob`, `section_2_rev_a.blob`, `section_3_rev_a.blob`, and `section_3_rev_b.blob`
- Have the ability to consume the data by programmatically saying "I want to download all of the `.blob` files that correspond with Hull X"
- Receive a notification whenever a new Revision is published to the database.

## Instructions

### Local

1. Install `nats` and `nats-server`. Instructions [here](https://docs.nats.io/nats-concepts/what-is-nats/walkthrough_setup).
2. Stand up a NATS server
    ```shell
   nats-server -js
    ```
3. Add an Object Store Bucket
    ```shell
    nats object add sections
    ```
4. Load the Sections and the State Index into the bucket
```shell
cd examples/object-store-with-pub-sub/data
nats object put sections section_1_rev_a.blob
nats object put sections section_2_rev_a.blob
nats object put sections section_3_rev_a.blob
nats object put sections section_3_rev_b.blob
nats object put sections state_index.yaml
```

### Kubernetes-based with Zarf

TODO: build this
