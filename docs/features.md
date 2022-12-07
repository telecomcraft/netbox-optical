# Features

## Optical Networking Fields

### Cable Fields

#### Fiber Type
The `fiber_type` custom field with a data type of Selection is added to the `dcim.cable` content type. This field is
used to indicate the specific ITU fiber type (such as G.652D) of the cable using pre-defined choices.

#### Power Loss
The `power_loss` custom field with a data type of Decimal is added to the `dcim.cable` content type. This field is used
to calculate the optical power loss of the cable using a configurable attenuation coefficient.

### Port Fields

#### Insertion Loss
The `insertion_loss` custom field with a data type of Decimal is added to the `dcim.front_port` and `dcim.rear_port`
content types. This field is used to calculate the optical insertion loss of mating a patch cord to a front or rear port.

#### Attenuator Loss
The `attenuator_loss` custom field with a data type of Decimal is added to the `dcim.front_port` and `dcim.rear_port`
content types. This field is used to calculate the optical insertion loss of an attenuator placed on a device's front or
rear port.

#### Return Loss
The `return_loss` custom field with a data type of Decimal is added to the `dcim.front_port` and `dcim.rear_port`
content types. This field is used to calculate the optical return loss of mating a patch cord to a device's front or
rear port.

### Interface Fields

#### Maximum TX Power
The `max_tx_power` custom field with a data type of Decimal is added to the `dcim.interface` content type. This field is
used to calculate the maximum optical power of a device's transceiver.

#### Minimum TX Power
The `max_tx_power` custom field with a data type of Decimal is added to the `dcim.interface` content type. This field is
used to calculate the minimum optical power of a device's transceiver.

#### RX Overload Threshold
The `rx_overload` custom field with a data type of Decimal is added to the `dcim.interface` content type. This field
is  used to calculate the receiver overload threshold of a device's transceiver.

#### RX Sensitivity Threshold
The `rx_sensitivity` custom field with a data type of Decimal is added to the `dcim.interface` content type. This field
is used to calculate the receiver sensitivity threshold of a device's transceiver.

#### TX Wavelength
The `tx_wavelength` custom field with a data type of Decimal is added to the `dcim.interface` content type. This field
is used to calculate the TX wavelength of a device's transceiver. If the transceiver is bi-directional (Bi-Di), simply
set both the TX and RX wavelength fields to the same value.

#### RX Wavelength
The `rx_wavelength` custom field with a data type of Decimal is added to the `dcim.interface` content type. This field
is used to calculate the RX wavelength of a device's transceiver. If the transceiver is bi-directional (Bi-Di), simply
set both the TX and RX wavelength fields to the same value.

## Optical Networking Calculations