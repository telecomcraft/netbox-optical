# Introduction

In a nutshell, optical networking is focused on the parts of the network where electrical signals are converted to and
transmitted as photonic signals to transport data between devices. This includes whenever data travels through
transceivers connected to fiber optic patch cords between equipment in the same data center, or when that data must
first travel across continents and oceans to reach its destination.

Maintaining records for optical network elements is just as important as any other aspect of network engineering in a
data center information manager (DCIM). DCIMs help you keep track of sites, racks, equipment, and cabling to exacting
detail, and Netbox remains a leading solution, evolving along with its users' needs year after year. Except for when
it came to certain situations regarding optical networking.

## What Made Optical Network Modeling Different?

Before now, accurately modeling duplex (or higher-count) patch cords and breakout cables (of all media types) in
Netbox wasn’t possible, so documentation beyond the initial equipment cord attached to the transceivers broke down
within patch panels and other optical link components. This also made it difficult to properly model splitters,
mux/demux modules, OADMs, and other passive components that are essential in optical networks.

Cables couldn’t be edited, either, so any changes to link configurations required deleting and recreating cable
records. This isn’t a blocking issue in and of itself, but because proper selection, installing, and testing of
optical cables is involving, and ideally should include tracking of optical loss and cleaning/inspection data,
having these records destroyed during Move-Add-Change (MAC) activities adds extra time to record keeping and
discourages thorough cable documentation.

Modeling active optical devices was tricky, too. Historically, devices with modular components such as line cards or
management modules had to be represented as separate, distinct devices in device bays. A GPON optical line terminal
(OLT), for example, often has multiple line cards, which would be represented as separate devices, even though they
weren’t. Also, Netbox lacked some of the interface types unique to optical devices, such as GPON and XGS-PON, so
interface types and their characteristics wouldn’t be correct.

With the releases of Netbox 3.2 and 3.3, however, all this has been resolved. Thanks to the Netbox development team’s
hard work on [issue #9102, “Extending the cable model to support multiple terminations,”](https://github.com/netbox-community/netbox/issues/9102)
and [issue 7844 “Introduce a model for device modules/line cards”](https://github.com/netbox-community/netbox/issues/7844),
all the above challenges appear to have been addressed, and proper optical modeling should be able to now take place.

Here are two videos with Netbox’s creator and lead developer, [Jeremy Stretch](https://packetlife.net/), giving a basic
demonstration of these changes:

[Netbox lead developer Jeremy Stretch presenting the new module functionality of Netbox 3.2.](https://www.youtube.com/watch?v=pIIqc31Mbwc)

Netbox lead developer Jeremy Stretch presenting the new module functionality of Netbox 3.2.

[Netbox lead developer Jeremy Stretch presenting the new multi-termination cabling functionality of Netbox 3.3.](https://www.youtube.com/watch?v=5JQlApaS8gM)

Netbox lead developer Jeremy Stretch presenting the new multi-termination cabling functionality of Netbox 3.3.

For years we’ve been using some creative workarounds, but I think it’s time to demonstrate the modern way to model
optical networks—in a vendor neural way—that accurately represents the system and can provide better documentation for
ongoing operational support and automation. In this series or articles I will demonstrate those approaches while
highlighting remaining challenges and possible workarounds.