# Generated by Django 4.0.3 on 2022-04-10 23:02

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AutomaticEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Nova Senha')], default=1, help_text='Determina do tipo de e-mail  que este registro representa.', unique=True, verbose_name='Tipo de E-mail')),
                ('subject', models.CharField(max_length=60, verbose_name='E-mail Subject')),
                ('text', models.TextField(help_text="Text which will be presented in the e-mail's body.<br/>Tags may be used to dynamically insert other content in the e-mail's body.<br/><br/>Tag list:<br/>- General:<br/>--- {user} (will insert an username of the client)<br/>--- {client_name} (will insert the client's full name)<br/>--- {list_client_names} (will insert a list of all client names)<br/>--- {document_name} (will insert the name of the document evaluated)<br/>- Checklist Section Refused:<br/>--- {checklist_refused_section} (will insert the name of the checklist section that was refused)<br/>--- {checklist_refused_reason} (will insert the reason for checklist section being refused)<br/>- Password Changed by Admin & New Password:<br/>--- {password_token_url} (will insert the link to a form that allows the user to redefine his password)<br/>- Alerts:<br/>--- {section_label} (will insert the name of the section completed)<br/>--- {receipt_document_name} (will insert the name of the document which the client has sent a receipt of)<br/>--- {rating} (will insert the rating of the client as declared by compliance)<br/>--- {compliance_user} (will insert the name of the compliance user involved in the event, if any)<br/>--- {compliance_evaluation_reason} (will insert the reason for approval or refusal of the client as written by the compliance user)<br/>--- {document_status} (will insert the evaluation status of the document, approved or refused)<br/>--- {document_evaluation_reason} (will insert the reason for approval or refusal of the document as written by the compliance/sales user)<br/>--- {manager_section} (will insert the name of which section the client was approved/refused in by a manager)<br/>--- {manager_evaluation_reason} (will insert the reason of the approval/refusal as stated by the manager)<br/>--- {funds_value} (will insert the value in funds of the client  as inputted by the client services user)<br/>--- {funds_currency} (will insert the currency of the client as inputted by the client services user)<br/>--- {funds_info} (will insert any additional info of the client's funds as inputted by the client services user)<br/>--- {otc_pf_number} (will insert the client's OTC Portfolio Number)<br/>--- {mcm_inc_pf_number} (will insert the client's MCM Inc. Portfolio Number)<br/>--- {mcm_ltd_pf_number} (will insert the client's MCM Ltd. Portfolio Number)<br/>--- {dtvm_pf_number} (will insert the client's DTVM Portfolio Number)<br/>--- {credit_reason} (will insert the reason for approval/refusal of credit facility)<br/>--- {credit_im_value} (will insert the client's Initial Margin Credit Value)<br/>--- {credit_iv_value} (will insert the client's Variation Margin Credit Value)<br/>--- {client_desk} (will insert the desk the client has chosen to work with)<br/>--- {products_add_docs_list} (will insert the list of products/assets that the client has chosen which require additional documentation)<br/>- Additional Document Approval:<br/>--- {add_doc_product} (will insert the name of the product associated with the approved additional document)<br/>- Password Changing by Email:<br/>--- {email_password_changing_token} (will insert the token for password changing that will be sent by email to the client)<br/>- Revalidation by Email:<br/>--- {email_revalidation_token} (will insert the token for revalidation that will be sent by email to the client)<br/><br/>Please make sure the tags are correct, and in the correct type of e-mail, as they may cause the e-mail body content to be incorrect if they are not.", verbose_name='E-mail Texto')),
                ('html', models.TextField(blank=True, help_text="HTML Content which will be presented in the e-mail's body.<br/><br/>Tags may be used to dynamically insert other content in the e-mail's body, and work exactly as they do in the above field.", null=True, verbose_name='E-mail HTML Content')),
                ('delay', models.FloatField(default=1, help_text='Define o intervalo de delay entre o envio de múltiplos emails deste tipo.', validators=[core.models.float_zero_ou_positivo], verbose_name='Delay entre emails')),
            ],
            options={
                'verbose_name': 'Configuraçao E-mail Automatico',
                'verbose_name_plural': 'Configuraçao E-mails Automaticos',
            },
        ),
    ]
