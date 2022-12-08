from django.contrib.contenttypes.models import ContentType

from extras.choices import CustomFieldTypeChoices
from extras.models.customfields import CustomField
from extras.scripts import Script


name = 'Netbox Optical Setup (0.8)'


# We'll need the IDs of the content types we will attach the custom
# fields to.
cable_id = ContentType.objects.get(model='cable').id
interface_id = ContentType.objects.get(model='interface').id
frontport_id = ContentType.objects.get(model='frontport').id
rearport_id = ContentType.objects.get(model='rearport').id
circuit_id = ContentType.objects.get(model='circuit').id

# Based on FOA link below and OTT CONA, CONE manuals
# https://www.thefoa.org/tech/smf.htm

# TODO: Add specialty fibers
FIBER_TYPES = (
    'G.651.1',
    'G.652',
    'G.652.B',
    'G.652.D',
    'G.653',
    'G.653.A',
    'G.653.B',
    'G.654',
    'G.654.A',
    'G.654.B',
    'G.654.C',
    'G.654.D',
    'G.654.E',
    'G.655',
    'G.655.C',
    'G.655.D',
    'G.655.E',
    'G.656',
    'G.657',
    'G.657.A1',
    'G.657.A2',
    'G.657.B2',
    'G.657.B3'
)


def get_optical_fields():
    fields = CustomField.objects.filter(group_name='Optical Settings')
    return fields


class CreateCustomFieldsScript(Script):

    class Meta:
        name = "Create Optical Networking Custom Fields"
        description = "Creates the optical networking custom fields"
        commit_default = True

    def run(self, data, commit):

        # TODO: Add exception check to ensure these fields don't already exist

        if CustomField.objects.filter(name='fiber_type').exists():
            self.log_failure('fiber_type custom field already exists')
        else:
            fiber_type = CustomField.objects.create(
                name='fiber_type',
                label='Fiber Type',
                group_name='Optical Settings',
                type=CustomFieldTypeChoices.TYPE_SELECT,
                # TODO: Add choices, defaults
                description="The ITU fiber type of the cable.",
                choices=FIBER_TYPES,
                # TODO: Is there a better way to reference this?
                # TODO: Any other MM?
                default="G.652"
            )
            fiber_type.content_types.set([cable_id])
            fiber_type.save()
            self.log_info("fiber_type custom field created")

        if CustomField.objects.filter(name='attenuation_coeff').exists():
            self.log_failure('attenuation_coeff custom field already exists')
        else:
            attenuation_coeff = CustomField.objects.create(
                name='attenuation_coeff',
                label='Attn Coeff',
                group_name='Optical Settings',
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The attenuation coefficient of the cable per km",
                choices=FIBER_TYPES,
                # TODO: Convert unit as needed, but always based on km
                default="0.4",  # TODO: Make configurable in config
            )
            attenuation_coeff.content_types.set([cable_id])
            attenuation_coeff.save()
            self.log_info("attenuation_coeff custom field created")

        if CustomField.objects.filter(name='power_loss').exists():
            self.log_failure('power_loss custom field already exists')
        else:
            power_loss = CustomField.objects.create(
                name='power_loss',
                label='Pwr Loss',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The overall power loss on the fiber across the cable's length.",
                validation_minimum=-60,  # Loss stops at -60 dB (0.000001)
                validation_maximum=0  # Loss starts at 0 dB (anything higher
                                      # isn't loss!
            )
            power_loss.content_types.set([cable_id])
            power_loss.save()
            self.log_info("power_loss custom field created")

        if CustomField.objects.filter(name='attenuator_loss').exists():
            self.log_failure('attenuator_loss custom field already exists')
        else:
            attenuator_loss = CustomField.objects.create(
                name='attenuator_loss',
                label='Attn Loss',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_INTEGER,
                description="The intentionally-added optical loss on this port from a fixed or variable attenuator.",
                validation_minimum=-60,  # Loss stops at -60 dB (0.000001)
                validation_maximum=0  # Loss starts at 0 dB (anything higher
                                      # isn't loss!
            )
            attenuator_loss.content_types.set([frontport_id, rearport_id])
            attenuator_loss.save()
            self.log_info("attenuator_loss custom field created")

        if CustomField.objects.filter(name='insertion_loss').exists():
            self.log_failure('insertion_loss custom field already exists')
        else:
            insertion_loss = CustomField.objects.create(
                name='insertion_loss',
                label='Ins Loss',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The optical loss caused by passing through the port",
                validation_minimum=-60,  # Loss stops at -60 dB (0.000001)
                validation_maximum=0  # Loss starts at 0 dB (anything higher
                                      # isn't loss!
            )
            insertion_loss.content_types.set([frontport_id, rearport_id])
            insertion_loss.save()
            self.log_info("insertion_loss custom field created")

        if CustomField.objects.filter(name='return_loss').exists():
            self.log_failure('return_loss custom field already exists')
        else:
            return_loss = CustomField.objects.create(
                name='return_loss',
                label='Rtn Loss',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The optical loss from reflection at the port",
                validation_minimum=-60,  # Loss stops at -60 dB (0.000001)
                validation_maximum=0  # Loss starts at 0 dB (anything higher
                                      # isn't loss!
            )
            return_loss.content_types.set([frontport_id, rearport_id])
            return_loss.save()
            self.log_info("return_loss custom field created")

        if CustomField.objects.filter(name='max_tx_power').exists():
            self.log_failure('max_tx_power custom field already exists')
        else:
            max_tx_power = CustomField.objects.create(
                name='max_tx_power',
                label='Max TX Pwr',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The maximum transmission power of the transceiver"
                # TODO: Add validation
            )
            max_tx_power.content_types.set([interface_id])
            max_tx_power.save()
            self.log_info("max_tx_power custom field created")

        if CustomField.objects.filter(name='min_tx_power').exists():
            self.log_failure('min_tx_power custom field already exists')
        else:
            min_tx_power = CustomField.objects.create(
                name='min_tx_power',
                label='Min TX Pwr',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The minimum transmission power of the transceiver"
                # TODO: Add validation
            )
            min_tx_power.content_types.set([interface_id])
            min_tx_power.save()
            self.log_info("min_tx_power custom field created")

        if CustomField.objects.filter(name='rx_overload').exists():
            self.log_failure('rx_overload custom field already exists')
        else:
            rx_overload = CustomField.objects.create(
                name='rx_overload',
                label='RX Ovld',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The overload power threshold of the transceiver"
                # TODO: Add validation
            )
            rx_overload.content_types.set([interface_id])
            rx_overload.save()
            self.log_info("rx_overload custom field created")

        if CustomField.objects.filter(name='rx_sensitivity').exists():
            self.log_failure('rx_sensitivity custom field already exists')
        else:
            rx_sensitivity = CustomField.objects.create(
                name='rx_sensitivity',
                label='RX Sen',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The sensitivity power threshold of the transceiver"
                # TODO: Add validation
            )
            rx_sensitivity.content_types.set([interface_id])
            rx_sensitivity.save()
            self.log_info("rx_sensitivity custom field created")

        if CustomField.objects.filter(name='tx_wavelength').exists():
            self.log_failure('tx_wavelength custom field already exists')
        else:
            tx_wavelength = CustomField.objects.create(
                name='tx_wavelength',
                label='TX Wave',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The specific TX wavelength of the transceiver",
                # FIXME: Integer fields are a limitation here; need <= option
                # and/or Decimal support
                validation_minimum=1260,  # Use start of the O-band
                # End right after the U-band (maybe we can prevent 1676 somehow?)
                validation_maximum=1676
            )
            tx_wavelength.content_types.set([interface_id])
            tx_wavelength.save()
            self.log_info("tx_wavelength custom field created")

        if CustomField.objects.filter(name='rx_wavelength').exists():
            self.log_failure('rx_wavelength custom field already exists')
        else:
            rx_wavelength = CustomField.objects.create(
                name='rx_wavelength',
                label='RX Wave',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The specific RX wavelength of the transceiver",
                # FIXME: Integer fields are a limitation here; need <= option
                # and/or Decimal support
                # TODO: Add MM (850)
                validation_minimum=1260,  # Use start of the O-band
                # End right after the U-band (maybe we can prevent 1676 somehow?)
                validation_maximum=1676
            )
            rx_wavelength.content_types.set([interface_id])
            rx_wavelength.save()
            self.log_info("rx_wavelength custom field created")

        # Return the output to the script page
        self.log_success('Generation of custom fields complete')


class UpdateCustomFieldsScript(Script):

    class Meta:
        name = "Update Optical Networking Custom Fields"
        description = "Updates the optical networking custom fields"
        commit_default = False

    def run(self, data, commit):

        fiber_type = CustomField.objects.get(name='fiber_type')
        fiber_type.label = 'Fiber Type'
        fiber_type.group_name = 'Optical Settings'
        fiber_type.type = CustomFieldTypeChoices.TYPE_SELECT
        fiber_type.description = "The ITU fiber type of the cable."
        fiber_type.choices = FIBER_TYPES
        fiber_type.default = "G.652"
        fiber_type.content_types.set([cable_id])
        fiber_type.save()
        self.log_info("fiber_type custom field updated")

        attenuation_coeff = CustomField.objects.get(name='attenuation_coeff')
        attenuation_coeff.label = 'Attn Coeff'
        attenuation_coeff.group_name = 'Optical Settings'
        attenuation_coeff.type = CustomFieldTypeChoices.TYPE_TEXT
        attenuation_coeff.description = "The attenuation coefficient of the cable per km"
        attenuation_coeff.choices = FIBER_TYPES
        attenuation_coeff.default = "0.4"
        attenuation_coeff.content_types.set([cable_id])
        attenuation_coeff.save()
        self.log_info("attenuation_coeff custom field updated")

        power_loss = CustomField.objects.get(name='power_loss')
        power_loss.label = 'Pwr Loss'
        power_loss.group_name = 'Optical Settings'
        power_loss.type = CustomFieldTypeChoices.TYPE_TEXT
        power_loss.description = "The overall power loss on the fiber across the cable's length."
        power_loss.validation_minimum = -60
        power_loss.validation_maximum = 0
        power_loss.content_types.set([cable_id])
        power_loss.save()
        self.log_info("power_loss custom field updated")

        attenuator_loss = CustomField.objects.get(name='attenuator_loss')
        attenuator_loss.label = 'Attn Loss'
        attenuator_loss.group_name = 'Optical Settings'
        attenuator_loss.type = CustomFieldTypeChoices.TYPE_INTEGER
        attenuator_loss.description = "The intentionally-added optical loss on this port from a fixed or variable attenuator."
        attenuator_loss.validation_minimum = -60
        attenuator_loss.validation_maximum = 0
        attenuator_loss.content_types.set([frontport_id, rearport_id])
        attenuator_loss.save()
        self.log_info("attenuator_loss custom field updated")

        insertion_loss = CustomField.objects.get(name='insertion_loss')
        insertion_loss.label = 'Ins Loss'
        insertion_loss.group_name = 'Optical Settings'
        insertion_loss.type = CustomFieldTypeChoices.TYPE_TEXT
        insertion_loss.description = "The optical loss caused by passing through the port"
        insertion_loss.validation_minimum = -60
        insertion_loss.validation_maximum = 0
        insertion_loss.content_types.set([frontport_id, rearport_id])
        insertion_loss.save()
        self.log_info("insertion_loss custom field updated")

        return_loss = CustomField.objects.get(name='return_loss')
        return_loss.label = 'Rtn Loss'
        return_loss.group_name = 'Optical Settings'
        return_loss.type = CustomFieldTypeChoices.TYPE_TEXT
        return_loss.description = "The optical loss from reflection at the port"
        return_loss.validation_minimum = -60
        return_loss.validation_maximum = 0
        return_loss.content_types.set([frontport_id, rearport_id])
        return_loss.save()
        self.log_info("return_loss custom field updated")

        max_tx_power = CustomField.objects.get(name='max_tx_power')
        max_tx_power.label = 'Max TX Pwr'
        max_tx_power.group_name = 'Optical Settings'
        max_tx_power.type = CustomFieldTypeChoices.TYPE_TEXT
        max_tx_power.description = "The maximum transmission power of the transceiver"
        max_tx_power.content_types.set([interface_id])
        max_tx_power.save()
        self.log_info("max_tx_power custom field updated")

        min_tx_power = CustomField.objects.get(name='min_tx_power')
        min_tx_power.label = 'Min TX Pwr'
        min_tx_power.group_name = 'Optical Settings'
        min_tx_power.type = CustomFieldTypeChoices.TYPE_TEXT
        min_tx_power.description = "The minimum transmission power of the transceiver"
        min_tx_power.content_types.set([interface_id])
        min_tx_power.save()
        self.log_info("min_tx_power custom field updated")

        rx_overload = CustomField.objects.get(name='rx_overload')
        rx_overload.label = 'RX Ovld'
        rx_overload.group_name = 'Optical Settings'
        rx_overload.type = CustomFieldTypeChoices.TYPE_TEXT
        rx_overload.description = "The overload power threshold of the transceiver"
        rx_overload.content_types.set([interface_id])
        rx_overload.save()
        self.log_info("rx_overload custom field updated")

        rx_sensitivity = CustomField.objects.get(name='rx_sensitivity')
        rx_sensitivity.label = 'RX Sen'
        rx_sensitivity.group_name = 'Optical Settings'
        rx_sensitivity.type = CustomFieldTypeChoices.TYPE_TEXT
        rx_sensitivity.description = "The sensitivity power threshold of the transceiver"
        rx_sensitivity.content_types.set([interface_id])
        rx_sensitivity.save()
        self.log_info("rx_sensitivity custom field updated")

        tx_wavelength = CustomField.objects.get(name='tx_wavelength')
        tx_wavelength.label = 'TX Wave'
        tx_wavelength.group_name = 'Optical Settings'
        tx_wavelength.type = CustomFieldTypeChoices.TYPE_TEXT
        tx_wavelength.description = "The specific TX wavelength of the transceiver"
        tx_wavelength.validation_minimum = 850
        tx_wavelength.validation_maximum = 1676
        tx_wavelength.content_types.set([interface_id])
        tx_wavelength.save()
        self.log_info("tx_wavelength custom field updated")

        rx_wavelength = CustomField.objects.get(name='rx_wavelength')
        rx_wavelength.label = 'RX Wave'
        rx_wavelength.group_name = 'Optical Settings'
        rx_wavelength.type = CustomFieldTypeChoices.TYPE_TEXT
        rx_wavelength.description = "The specific RX wavelength of the transceiver"
        rx_wavelength.validation_minimum = 850
        rx_wavelength.validation_maximum = 1676
        rx_wavelength.content_types.set([interface_id])
        rx_wavelength.save()
        self.log_info("rx_wavelength custom field updated")

        self.log_success('All optical fields updated')


class RemoveCustomFieldsScript(Script):

    class Meta:
        name = "Remove Optical Networking Custom Fields"
        description = "Removes the optical networking custom fields"
        commit_default = False

    def run(self, data, commit):
        fields = get_optical_fields()

        for field in fields:
            CustomField.objects.filter(id=field.id).delete()
            self.log_info(f"{field.name} removed")

        self.log_success('All optical fields removed')


script_order = (
    CreateCustomFieldsScript,
    UpdateCustomFieldsScript,
    RemoveCustomFieldsScript
)
