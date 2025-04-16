# ExploreTech Founding Software Engineer 
## Phase II: Collaborative Coding Interview

### Instructions

Review the system overview and pick one of the three options below to start. Let's see how far we can get in an hour together! Make sure your dev environment is prepared beforehand and this repository is ready to go. We'll both be working on this together, so we'll need to figure out how to handle branches, merging, and division of labor to make sure it goes smooth. Use Cursor or ChatGPT all you want. You're in the driver's seat, so let me know how I can be most useful! 

### System Overview

The most basic architecture of our exploration product is shown in the figure below. Users are our own field teams, who are out in remote parts of the world collecting exploration data. They have a mobile device with them, which has a custom application that allows them to collect and send data to our servers. The servers process the data and send back decision recommendations. 

![Software Architecture](assets/simple-architecture-diagram.png)

For the purposes of this interview, we just need to pick one part of the stack and see how far we can get. More details on the 3 options are below.


### Option 1. Front-End

This can start as simple interface that has a form to fill out and submit a new dataset. A sample dataset is in `data/sample-induced-polarization-dataset.dat`. 


The basic functionality is:

- The user can create a new "entry".
- The entry is just a form with the following fields: name, date, and the file to be uploaded
- When the entry is submitted, the form data is validated and sent to the API (or at least for now printed to console)


For the purposes of this interview, this can be web or mobile. You can use whatever language and framework you like. Tests and documentation are encouraged.


### Option 2. REST API

Build a REST API that receives a data file, writes it to a filesystem, and sends it back to the user on command.

The basic functionality is:

- The API has a route to receive a dataset, plus metadata like a name and date of creation.
- The API can write the dataset to the server's filesystem.
- The API has a route to send a dataset back, plus metadata.
- For large files, the API handles chunking.

For the purposes of this interview, the API just needs to run on a simple HTTP protocol. Any language and framework is fine. Testing and documentation are encouraged.


### Option 3. Data Manipulation

Create a Python package (or equivalent in your preferred language) facilitates data manipulation. This package will be used across multiple parts of the product, including in the REST API and in data processing scripts written by the field teams. 

A sample dataset is in `data/sample-induced-polarization-dataset.dat`. This example is a text file, but the exact same data may be found in a binary file, a CSV, or a more exotic format, depending on how it was collected and processed.  

This type of data is called [Induced Polarization (IP)](https://em.geosci.xyz/content/geophysical_surveys/ip/index.html). It's collected by sending a strong electrical current into the ground through a transmitter (Tx), then measuring how much current is present across different parts of the property. The measurements are collected by receivers (Rx). Importantly, the data are collected in "lines", which is critical to understanding how the data are stored and processed (see the figure below).

![Induced Polarization Lines](assets/induced-polarization-example-figure.png)

**Specs:**
The package needs to facilitate the following actions:

- Reading datasets (max 1GB) from multiple formats (CSV, plain text, binary) into a single `InducedPolarizationSurvey` class.
- The ability to convert between file formats.
- Filtering the dataset based on Line Number, or other criteria
- Filtering the dataset spatially, based on transmitter or receiver locations.

**Documentation:** The package should be documented with a consistent format that can eventually be collected into a centralized documentation system.

**Testing:** The package should also have a thorough suite of tests, and instructions to help new developers run tests. 


### Bonus: Connect all 3 steps together!

Get the front-end to communicate with the API. The API will handle the file conversion and send the updated file back to the user's device on command. 