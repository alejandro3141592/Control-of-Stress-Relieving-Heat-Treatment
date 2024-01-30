# Control-of-Stress-Relieving-Heat-Treatment

This repository contains the work I made for the DUAL company. They wanted to create a monitoring system for the process of Stress Relieving Heat Treatment, so I developed a Python script that reads a node-red server connected to a PLC S7-1200 that acquired the data from the sensors, and then, uploaded it to the cloud of AWS using the service of Dynamo DB.

You can find more information about the algorithm I made in the codes folder.

In the following image, you can see part of the process, where the ladder code for the PLC is shown, and in the right upper corner, the HMI is displayed.

<p align="center">
<img src="https://github.com/alejandro3141592/Control-of-Stress-Relieving-Heat-Treatment/assets/132953325/c6d2359f-dc61-4dc3-89a4-a99b81cab077"/>
</p>


You can also see the database in the AWS cloud that was obtained in the following image.

<p align="center">
<img src="https://github.com/alejandro3141592/Control-of-Stress-Relieving-Heat-Treatment/assets/132953325/9f63e3b8-f45d-448a-9426-bca11969ea69"/>
</p>

In addition, I developed two electronic circuits needed to develop a control loop using the PLC. The first one acted as the signal conditioning stage, which transformed the analog signals of the type-K temperature sensors, into wider signals, making the reads of the PLC more precise. You can see an image of the schematic circuit below.
<p align="center">
<img src="https://github.com/alejandro3141592/Control-of-Stress-Relieving-Heat-Treatment/assets/132953325/3586a129-6486-4ea9-a5b8-287edd489729"/>
</p>

The other one acted as the power stage of the control loop, this circuit uses an external power supply used in welding that is capable of providing up to 40 Ampers, that is the one they used to work with when they controlled the process manually, so with this, a linear optocoupler, an Instrumentation Amplifier, and a high-power MOSFET, the feedback to the system was made. Below you can see the schematic of the circuit.

<p align="center">
<img src="https://github.com/alejandro3141592/Control-of-Stress-Relieving-Heat-Treatment/assets/132953325/db89ab57-49d3-4671-9008-991e5929e666"/>
</p>
