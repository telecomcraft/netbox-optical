from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from extras.choices import CustomFieldTypeChoices
from extras.models.customfields import CustomField
from extras.scripts import Script, StringVar, ObjectVar


name = 'Netbox Optical'


def get_optical_fields():
    fields = CustomField.objects.filter(
        Q(group_name='Optical Loss') | Q(group_name='Optical Power')
    )
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

        attenuation_coeff = CustomField.objects.create(
            name='attenuation_coeff',
            label='Attenuation Coefficient',
            group_name='Optical Loss',
            type=CustomFieldTypeChoices.TYPE_TEXT,  # This will change in Netbox 3.4 to Decimal
            description="The overall optical loss on the fiber across the cable's length"
        )
        attenuation_coeff.content_types.set([cable_id])
        attenuation_coeff.save()
        self.log_info("attenuation_coeff custom field created")

        attenuator_loss = CustomField.objects.create(
            name='attenuator_loss',
            label='Attenuator Loss',
            group_name='Optical Loss',
            type=CustomFieldTypeChoices.TYPE_INTEGER,  # This will change in Netbox 3.4 to Decimal
            description="The intentionally-added optical loss on this port from a fixed or variable attenuator"
        )
        attenuator_loss.content_types.set([frontport_id, rearport_id])
        attenuator_loss.save()
        self.log_info("attenuator_loss custom field created")

        insertion_loss = CustomField.objects.create(
            name='insertion_loss',
            label='Insertion Loss',
            group_name='Optical Loss',
            type=CustomFieldTypeChoices.TYPE_TEXT,  # This will change in Netbox 3.4 to Decimal
            description="The optical loss passing through the port"
        )
        insertion_loss.content_types.set([frontport_id, rearport_id])
        insertion_loss.save()
        self.log_info("insertion_loss custom field created")

        return_loss = CustomField.objects.create(
            name='return_loss',
            label='Return Loss',
            group_name='Optical Loss',
            type=CustomFieldTypeChoices.TYPE_TEXT,  # This will change in Netbox 3.4 to Decimal
            description="The optical loss from reflection at the port"
        )
        return_loss.content_types.set([frontport_id, rearport_id])
        return_loss.save()
        self.log_info("return_loss custom field created")

        max_tx_power = CustomField.objects.create(
            name='max_tx_power',
            label='Maximum TX Power',
            group_name='Optical Power',
            type=CustomFieldTypeChoices.TYPE_TEXT,  # This will change in Netbox 3.4 to Decimal
            description="The maximum transmission power of the transceiver"
        )
        max_tx_power.content_types.set([interface_id])
        max_tx_power.save()
        self.log_info("max_tx_power custom field created")

        min_tx_power = CustomField.objects.create(
            name='min_tx_power',
            label='Minimum TX Power',
            group_name='Optical Power',
            type=CustomFieldTypeChoices.TYPE_TEXT,  # This will change in Netbox 3.4 to Decimal
            description="The minimum transmission power of the transceiver"
        )
        min_tx_power.content_types.set([interface_id])
        min_tx_power.save()
        self.log_info("min_tx_power custom field created")

        rx_overload = CustomField.objects.create(
            name='rx_overload',
            label='RX Overload',
            group_name='Optical Power',
            type=CustomFieldTypeChoices.TYPE_TEXT,  # This will change in Netbox 3.4 to Decimal
            description="The overload power threshold of the transceiver"
        )
        rx_overload.content_types.set([interface_id])
        rx_overload.save()
        self.log_info("rx_overload custom field created")

        rx_sensitivity = CustomField.objects.create(
            name='rx_sensitivity',
            label='RX Sensitivity',
            group_name='Optical Power',
            type=CustomFieldTypeChoices.TYPE_TEXT,  # This will change in Netbox 3.4 to Decimal
            description="The sensitivity power threshold of the transceiver"
        )
        rx_sensitivity.content_types.set([interface_id])
        rx_sensitivity.save()
        self.log_info("rx_sensitivity custom field created")

        tx_wavelength = CustomField.objects.create(
            name='tx_wavelength',
            label='TX Wavelength',
            group_name='Optical Power',
            type=CustomFieldTypeChoices.TYPE_TEXT,
            # This will change in Netbox 3.4 to Decimal
            description="The specific TX wavelength of the transceiver"
        )
        tx_wavelength.content_types.set([interface_id])
        tx_wavelength.save()
        self.log_info("tx_wavelength custom field created")

        rx_wavelength = CustomField.objects.create(
            name='rx_wavelength',
            label='RX Wavelength',
            group_name='Optical Power',
            type=CustomFieldTypeChoices.TYPE_TEXT,  # This will change in Netbox 3.4 to Decimal
            description="The specific RX wavelength of the transceiver"
        )
        rx_wavelength.content_types.set([interface_id])
        rx_wavelength.save()
        self.log_info("rx_wavelength custom field created")

        # Return the output to the script page
        self.log_success('Generation of custom fields complete')

# TODO: Change script order


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
