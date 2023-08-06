# LUPUSEC XT2 (Client)

[![Test](https://github.com/ChrisKeck/lupuxt2py/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/ChrisKeck/lupuxt2py/actions/workflows/test.yml)

Python-Library to communicate and interface with Lupusec X2 System.

API-CALLs to Lupusec XT2 with LupusecSevice:

* GET /action/deviceGet -> return dictionary with device class as key and lists of specific type as value
* GET /action/systemGet -> return system information
* GET /action/panelCondGet -> return alarm panels and updates
* POST /action/panelCondPost -> activate/deactivate alarm mode
* POST /action/deviceSwitchPSSPost -> switch on/off something


Poll Lupusec XT2 in a timeloop with LupusecStateMachine

# Attention
I can only support devices, which I have on my own! Todos if anyone would like to add a device:

* Add a sample response to folder tests/responses
* Add unit-tests to folder tests 
