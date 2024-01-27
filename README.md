# Intelligent_irrigation_system
_**Python Diploma Project**_

This project is dedicated to creating a prototype of a control module for an intelligent drip irrigation system. In the project, both the front-end and back-end were implemented:
- The front-end implementation utilized the Django framework.
- The back-end implementation consists of capturing images via the Onvif protocol from a camera, classification based on a pre-trained convolutional neural network ResNet-18, and irrigation control via the Modbus protocol. The database used is SQLite.

The work is divided into the following subtasks:
1.	Development of the database structure.
2.	Development of the processing module, consisting of submodules.
3.	Development of the user web interface.
4.	Conducting testing and analysis of the work done.

The scope of work does not include:
- Implementation of the image acquisition system/camera control.
- Implementation of the irrigation system.

Interaction with these systems is carried out through respective APIs.

![Project_Structure](https://github.com/natkhosh/Intelligent_irrigation_system/assets/56446265/0e74fea8-e622-46a5-9a66-de234d948911)

Having reviewed the requirements for such systems, I have drafted the Technical Specification. The main functional requirements include:
- Capturing images from a camera moving through warehouse positions.
- Processing the image and determining the plant type.
- Retrieving information from the database for irrigation according to the determined plant class.
- Issuing commands for irrigation.
- Collecting statistics for analytics.
- Web interface for configuring irrigation parameters and displaying statistics.

The diagram illustrates the sequence of interaction between the main modules.

![Interaction_scenarios](https://github.com/natkhosh/Intelligent_irrigation_system/assets/56446265/39c07ea2-9001-46a8-8d56-47a625a3f460)
