# Control-of-Stress-Relieving-Heat-Treatment

This repository contains the work I made for the DUAL company. They wanted to create a monitoring system for the process of Stress Relieving Heat Treatment, so I developed a Python script that reads a node-red server connected to a PLC S7-1200 that acquired the data from the sensors, and then, uploaded it to the cloud of AWS using the service of Dynamo DB.

You can find more information about the algorithm I made in the codes folder.

In the following image, you can see part of the process, where the ladder code for the PLC is shown, and in the right upper corner, the HMI is displayed.

You can also see the database in the AWS cloud that was obtained in the following image.


In addition, I developed two electronic circuits needed to develop a control loop using the PLC. The first one acted as the signal conditioning stage, which transformed the analog signals of the type-K temperature sensors, into wider signals, making the reads of the PLC more precise. You can see an image of the schematic circuit below.


The other one acted as the power stage of the control loop, this circuit uses an external power supply used in welding that is capable of providing up to 40 Ampers, that is the one they used to work with when they controlled the process manually, so with this, a linear optocoupler, an Instrumentation Amplifier, and a high-power MOSFET, the feedback to the system was made. Below you can see the schematic of the circuit.

