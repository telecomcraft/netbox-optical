from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError

from extras.choices import CustomFieldTypeChoices
from extras.models.customfields import CustomField
from extras.scripts import Script, StringVar, ObjectVar


name = 'Netbox Optical Setup (0.3)'

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

        # We'll need the IDs of the content types we will attach the custom
        # fields to.
        cable_id = ContentType.objects.get(model='cable').id
        interface_id = ContentType.objects.get(model='interface').id
        frontport_id = ContentType.objects.get(model='frontport').id
        rearport_id = ContentType.objects.get(model='rearport').id
        circuit_id = ContentType.objects.get(model='circuit').id

        # TODO: Add exception check to ensure these fields don't already exist

        if CustomField.objects.filter(name='fiber_type'):
            self.log_failure('fiber_type custom field already exists')
        else:
            fiber_type = CustomField.objects.create(
                name='fiber_type',
                label='Fiber Type',
                group_name='Optical Settings',
                type=CustomFieldTypeChoices.TYPE_SELECT,
                # TODO: Add choices, defaults
                description="The ITU fiber type of the cable.",
                choices=FIBER_TYPES
            )
            fiber_type.content_types.set([cable_id])
            fiber_type.save()
            self.log_info("fiber_type custom field created")

        if CustomField.objects.filter(name='power_loss'):
            self.log_failure('power_loss custom field already exists')
        else:
            power_loss = CustomField.objects.create(
                name='power_loss',
                label='Power Loss',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The overall power loss on the fiber across the cable's length."
            )
            power_loss.content_types.set([cable_id])
            power_loss.save()
            self.log_info("power_loss custom field created")

        if CustomField.objects.filter(name='attenuator_loss'):
            self.log_failure('attenuator_loss custom field already exists')
        else:
            attenuator_loss = CustomField.objects.create(
                name='attenuator_loss',
                label='Attenuator Loss',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_INTEGER,
                description="The intentionally-added optical loss on this port from a fixed or variable attenuator."
            )
            attenuator_loss.content_types.set([frontport_id, rearport_id])
            attenuator_loss.save()
            self.log_info("attenuator_loss custom field created")

        if CustomField.objects.filter(name='insertion_loss'):
            self.log_failure('insertion_loss custom field already exists')
        else:
            insertion_loss = CustomField.objects.create(
                name='insertion_loss',
                label='Insertion Loss',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The optical loss passing through the port"
            )
            insertion_loss.content_types.set([frontport_id, rearport_id])
            insertion_loss.save()
            self.log_info("insertion_loss custom field created")

        if CustomField.objects.filter(name='return_loss'):
            self.log_failure('return_loss custom field already exists')
        else:
            return_loss = CustomField.objects.create(
                name='return_loss',
                label='Return Loss',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The optical loss from reflection at the port"
            )
            return_loss.content_types.set([frontport_id, rearport_id])
            return_loss.save()
            self.log_info("return_loss custom field created")

        if CustomField.objects.filter(name='max_tx_power'):
            self.log_failure('max_tx_power custom field already exists')
        else:
            max_tx_power = CustomField.objects.create(
                name='max_tx_power',
                label='Maximum TX Power',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The maximum transmission power of the transceiver"
            )
            max_tx_power.content_types.set([interface_id])
            max_tx_power.save()
            self.log_info("max_tx_power custom field created")

        if CustomField.objects.filter(name='min_tx_power'):
            self.log_failure('min_tx_power custom field already exists')
        else:
            min_tx_power = CustomField.objects.create(
                name='min_tx_power',
                label='Minimum TX Power',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The minimum transmission power of the transceiver"
            )
            min_tx_power.content_types.set([interface_id])
            min_tx_power.save()
            self.log_info("min_tx_power custom field created")

        if CustomField.objects.filter(name='rx_overload'):
            self.log_failure('rx_overload custom field already exists')
        else:
            rx_overload = CustomField.objects.create(
                name='rx_overload',
                label='RX Overload',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The overload power threshold of the transceiver"
            )
            rx_overload.content_types.set([interface_id])
            rx_overload.save()
            self.log_info("rx_overload custom field created")

        if CustomField.objects.filter(name='rx_sensitivity'):
            self.log_failure('rx_sensitivity custom field already exists')
        else:
            rx_sensitivity = CustomField.objects.create(
                name='rx_sensitivity',
                label='RX Sensitivity',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The sensitivity power threshold of the transceiver"
            )
            rx_sensitivity.content_types.set([interface_id])
            rx_sensitivity.save()
            self.log_info("rx_sensitivity custom field created")

        if CustomField.objects.filter(name='tx_wavelength'):
            self.log_failure('tx_wavelength custom field already exists')
        else:
            tx_wavelength = CustomField.objects.create(
                name='tx_wavelength',
                label='TX Wavelength',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The specific TX wavelength of the transceiver"
            )
            tx_wavelength.content_types.set([interface_id])
            tx_wavelength.save()
            self.log_info("tx_wavelength custom field created")

        if CustomField.objects.filter(name='rx_wavelength'):
            self.log_failure('rx_wavelength custom field already exists')
        else:
            rx_wavelength = CustomField.objects.create(
                name='rx_wavelength',
                label='RX Wavelength',
                group_name='Optical Settings',
                # FIXME: Update to Decimal for Netbox 3.4
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The specific RX wavelength of the transceiver"
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
        fields = get_optical_fields()

        for field in fields:
            self.log_info(f"{field.name} updated")

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
