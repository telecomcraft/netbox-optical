from django.contrib.contenttypes.models import ContentType

from extras.choices import CustomFieldTypeChoices
from extras.models.customfields import CustomField
from extras.scripts import Script, StringVar, ObjectVar


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

        attenuation_coeff = CustomField(
            name='attenuation_coeff',
            label='Attenuation Coefficient',
            group_name='Optical Loss',
            type=CustomFieldTypeChoices.TYPE_TEXT,  # This will change in Netbox 3.4 to Decimal
            description="The overall optical loss on the cable's fiber"
        )
        attenuation_coeff.content_types.set([cable_id])
        self.log_info("attenuation_coeff custom field created")

        attenuator_loss = CustomField(
            name='attenuator_loss',
            label='Attenuator Loss',
            group_name='Optical Loss',
            type=CustomFieldTypeChoices.TYPE_INTEGER,  # This will change in Netbox 3.4 to Decimal
            description="The intentionally-added loss on the optical link from a fixed or variable attenuator"
        )
        attenuator_loss.content_types.set([frontport_id, rearport_id])
        self.log_info("attenuation_coeff custom field created")

        insertion_loss = CustomField(
            name='insertion_loss',
            label='Attenuator Loss',
            group_name='Optical Loss',
            type=CustomFieldTypeChoices.TYPE_TEXT,  # This will change in Netbox 3.4 to Decimal
            description="The intentionally-added loss on the optical link"
        )
        insertion_loss.content_types.set([frontport_id, rearport_id])
        self.log_info("insertion_loss custom field created")

        return_loss = CustomField(
            name='return_loss',
            label='Return Loss',
            group_name='Optical Loss',
            type=CustomFieldTypeChoices.TYPE_TEXT,  # This will change in Netbox 3.4 to Decimal
            description="The intentionally-added loss on the optical link"
        )
        return_loss.content_types.set([frontport_id, rearport_id])
        self.log_info("return_loss custom field created")

        max_tx_power = CustomField(
            name='max_tx_power',
            label='Maximum TX Power',
            group_name='Optical Loss',
            type=CustomFieldTypeChoices.TYPE_TEXT,  # This will change in Netbox 3.4 to Decimal
            description="The intentionally-added loss on the optical link"
        )
        max_tx_power.content_types.set([frontport_id, rearport_id])
        self.log_info("max_tx_power custom field created")

        min_tx_power = CustomField(
            name='min_tx_power',
            label='Minimum TX Power',
            group_name='Optical Loss',
            type=CustomFieldTypeChoices.TYPE_TEXT,  # This will change in Netbox 3.4 to Decimal
            description="The intentionally-added loss on the optical link"
        )
        min_tx_power.content_types.set([interface_id])
        self.log_info("min_tx_power custom field created")

        rx_overload = CustomField(
            name='rx_overload',
            label='RX Overload',
            group_name='Optical Loss',
            type=CustomFieldTypeChoices.TYPE_TEXT,  # This will change in Netbox 3.4 to Decimal
            description="The intentionally-added loss on the optical link"
        )
        rx_overload.content_types.set([interface_id])
        self.log_info("rx_overload custom field created")

        rx_sensitivity = CustomField(
            name='rx_sensitivity',
            label='RX Sensitivity',
            group_name='Optical Loss',
            type=CustomFieldTypeChoices.TYPE_TEXT,  # This will change in Netbox 3.4 to Decimal
            description="The intentionally-added loss on the optical link"
        )
        rx_sensitivity.content_types.set([interface_id])
        self.log_info("rx_sensitivity custom field created")

        rx_wavelength = CustomField(
            name='rx_wavelength',
            label='Attenuator Loss',
            group_name='Optical Loss',
            type=CustomFieldTypeChoices.TYPE_TEXT,  # This will change in Netbox 3.4 to Decimal
            description="The intentionally-added loss on the optical link"
        )
        rx_wavelength.content_types.set([interface_id])
        self.log_info("rx_wavelength custom field created")

        tx_wavelength = CustomField(
            name='tx_wavelength',
            label='Attenuator Loss',
            group_name='Optical Loss',
            type=CustomFieldTypeChoices.TYPE_TEXT,  # This will change in Netbox 3.4 to Decimal
            description="The intentionally-added loss on the optical link"
        )
        tx_wavelength.content_types.set([interface_id])
        self.log_info("tx_wavelength custom field created")

        # Return the output to the script page
        return attenuation_coeff
