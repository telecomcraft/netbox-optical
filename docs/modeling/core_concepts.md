# Core Optical Modeling Concepts

## Common Optical Network Modeling Use Cases

Optical network modeling can be categorized into **active optical devices** (such as routers, switches, OLTs,
ONUs/ONTs, Mux/Demuxers, ROADMs, amplifiers, etc.) and the **passive optical devices/cable plant** (patch cords,
backbone/distribution cables, adapters, attenuators, filters, splices, etc.) that connect the active devices.

Using the new Netbox functionality, we’ll model the active optical devices along with the necessary passive optical
cable plant to support that device application, along with the related other models such as sites, locations, racks,
etc. The common use cases for device to cable plant terminations can be categorized into two topologies: 

- **Point-to-point links**, such as simply interconnecting or cross-connecting two switches with simplex or duplex
patch and equipment cords.
- **Point-to-multipoint links**, where a breakout cable, splitter, mux/demux, or OADM would combine fiber strands on
one side, usually to attach to a transceiver, but then create multiple cable paths on the other side to route or
distribute signals in various ways.

We’ll provide examples of specific configurations for each type of topology in separate pages, but for now let’s
take a closer look at these two topologies before moving on.

### Point-to-Point (PTP) Circuit Modeling

Modeling optical point-to-point (or PTP for short) circuits in Netbox is straightforward. In a simple scenario, you
would define the devices on both sides of a circuit, their interfaces (such as modular SFP+ types), and then model
out the components of the fiber optic link in between.

In most cases this will start with a simplex or duplex (MMF or SMF) equipment cord, possibly patched into one or more
adapter panels via multiple equivalent patch cords, and then into the equipment cord and terminated at the interface
on the other side of the circuit. A key thing to remember is that there is always a 1:1 ratio of fiber strands across
the link between interfaces.

For a simplex link, you have one fiber on side A, and one fiber on side B. For a duplex link, you have two fibers on
side A, and two on side B. In both of these cases, the links will be modeled with corresponding simplex or duplex
termination points along the path of the link, such as through adapter panels or splice trays.

In some cases you’ll be using parallel optics to reach 40Gb/s or higher, via MPO or MPT cable plant. Here you’ll have
8, 12, 16, or even 24 fibers on side A, but still the same number on side B, keeping the 1:1 ratio between interfaces.
The importance difference here, however, it that if the cables are connectorized, you’ll using single specialized ports
for each termination, versus splicing each fiber if they are not connectorized.

For all of these cases we’ll still call this a point-to-point link, as there is only one transceiver on each side of
the circuit.

### Point to Multi-Point Circuit Modeling

Modeling optical point-to-multipoint (or PTMP for short) circuits in Netbox is where things get complicated. In these
scenarios, you define one device for the “point” side and multiple devices for the “multi-point” side of the circuit,
and then model out the components of the fiber optic link in between.

So what makes optical PTMP circuits unique? It’s that the optical transmissions are split up (and possibly
re-combined) within the link. Let’s quickly summarize a few common applications.

PON

DWDM Mux/Demux

ROADM


## Filling in Some Gaps with Custom Fields

| Field Name | Field Label | Content Types | Data Type |
| -- | --- |------------------|-------|
| `fiber_type` | Fiber Type | `dcim.cable` | Selection |
| `attn_coeff` | Attn Coeff | `dcim.cable` | Decimal |
| `power_loss` | Power Loss | `dcim.cable` | Decimal |
| `attn_loss` | Attn Loss | `dcim.front_port` & `dcim.rear_port` | Decimal |
| `insertion_loss` | Ins Loss | `dcim.front_port` & `dcim.rear_port` | Decimal |
| `return_loss` | Rtn Loss | `dcim.front_port` & `dcim.rear_port` | Decimal |
| `max_tx_power` | Max TX Pwr | `dcim.interface` | Decimal |
| `min_tx_power` | Min TX Pwr | `dcim.interface` | Decimal |
| `rx_overload` | RX Ovld | `dcim.interface` | Decimal |
| `rx_sensitivity` | RX Sen | `dcim.interface` | Decimal |
| `rx_wavelength` | RX Wave | `dcim.interface` | Decimal |
| `tx_wavelength` | TX Wave | `dcim.interface` | Decimal |