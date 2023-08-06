# requirements !pip install hubspot3 -q



import pytz
import pandas as pd

import requests
from hubspot3 import Hubspot3



"""

Description for get_deals_all_fiels function

MANDATORY INPUT: API_KEY

OPTIONAL INPUT: 

- n_days: number of range interval (interval goes from n_days ago up to today)
        default is n_days = 7 (last 7 days)


"""




def get_hubspot_deals_all_fiels(API_KEY, 
                        
                        #optional input
                        n_days = 7):
    
    from datetime import date as dt, timedelta as td , datetime, timezone

    url = "https://api.hubapi.com/crm/v3/objects/deals"

    start_date = (dt.today()-td(days=n_days)).isoformat()

    print("start {} days ago: {}".format(n_days, start_date))
    
    
    start_date = datetime.strptime(start_date,"%Y-%m-%d")

    y = 0

    i = 20
    after = '1'
    deals_all_fields_record = []


    while i >0 :
        # miss_tariffa___motivo_ko
        # miss_tariffa___motivo_trash
        # google_ad_click_id
        # contattabile

        if y%500 == 0:
            print(y)

        y += 1
        querystring = {"limit": "100", "paginateAssociations": "false" ,"properties":"tipo_di_ordine,miss_tariffa___motivo_ko,miss_tariffa___motivo_trash,google_ad_click_id,amount_in_home_currency,days_to_close,hs_acv,hs_analytics_source,hs_analytics_source_data_1,hs_analytics_source_data_2,hs_arr,campaign_name,hs_closed_amount,hs_closed_amount_in_home_currency,hs_created_by_user_id,hs_deal_stage_probability,hs_forecast_amount,hs_forecast_probability,hs_is_closed,hs_is_closed_won,hs_lastmodifieddate,hs_likelihood_to_close,hs_line_item_global_term_hs_discount_percentage,hs_line_item_global_term_hs_discount_percentage_enabled,hs_line_item_global_term_hs_recurring_billing_period,hs_line_item_global_term_hs_recurring_billing_period_enabled,hs_line_item_global_term_hs_recurring_billing_start_date,hs_line_item_global_term_hs_recurring_billing_start_date_enabled,hs_line_item_global_term_recurringbillingfrequency,hs_line_item_global_term_recurringbillingfrequency_enabled,hs_manual_forecast_category,hs_merged_object_ids,hs_mrr,hs_next_step,hs_object_id,hs_predicted_amount,hs_predicted_amount_in_home_currency,hs_projected_amount,hs_projected_amount_in_home_currency,hs_tcv,hs_time_in_appointmentscheduled,hs_time_in_closedlost,hs_time_in_closedwon,hs_time_in_contractsent,hs_time_in_decisionmakerboughtin,hs_time_in_presentationscheduled,hs_time_in_qualifiedtobuy,hs_unique_creation_key,hs_updated_by_user_id,hs_user_ids_of_all_owners,hubspot_owner_assigneddate,application_uuid3,dealname,salesforcelastsynctime,amount,dealstage,onboardingfrontlink,pipeline,closedate,onboardingadminlink,createdate,engagements_last_meeting_booked,engagements_last_meeting_booked_campaign,engagements_last_meeting_booked_medium,engagements_last_meeting_booked_source,hs_latest_meeting_activity,hs_sales_email_last_replied,hubspot_owner_id,notes_last_contacted,notes_last_updated,notes_next_activity_date,num_contacted_notes,num_notes,hs_createdate,hubspot_team_id,dealtype,hs_all_owner_ids,description,hs_all_team_ids,hs_all_accessible_team_ids,num_associated_contacts,closed_lost_reason,closed_won_reason,application_uuid2","after":after,
                    "archived": "false", "hapikey": API_KEY}

        headers = {'accept': 'application/json'}
        response = requests.request("GET", url, headers=headers, params=querystring)


        dati = response.json()
        try:
            after = dati['paging']['next']['after']
            i = len(dati['paging']['next']['after'])
        except:
            after = ''
            i = 0
        d1 = dati["results"]
        for dd in d1:
            try:
                id = dd['id']
            except :
                id = ''
            try:
                amount_in_home_currency = dd['properties']['amount_in_home_currency']
            except :
                amount_in_home_currency = ''
            try:
                days_to_close = dd['properties']['days_to_close']
            except :
                days_to_close = ''
            try:
                hs_acv = dd['properties']['hs_acv']
            except :
                hs_acv = ''

            try:
                hs_analytics_source = dd['properties']['hs_analytics_source']
            except :
                hs_analytics_source = ''

            try:
                tipo_di_ordine = dd['properties']['tipo_di_ordine']
            except :
                tipo_di_ordine = ''
            try:
                hs_analytics_source_data_1 = dd['properties']['hs_analytics_source_data_1']
            except :
                hs_analytics_source_data_1 = ''
            try:
                hs_analytics_source_data_2 = dd['properties']['hs_analytics_source_data_2']
            except :
                hs_analytics_source_data_2 = ''
            try:
                miss_tariffa___motivo_ko = dd['properties']['miss_tariffa___motivo_ko']
            except :
                miss_tariffa___motivo_ko = ''
            try:
                miss_tariffa___motivo_trash = dd['properties']['miss_tariffa___motivo_trash']
            except :
                miss_tariffa___motivo_trash = ''
            try:
                google_ad_click_id = dd['properties']['google_ad_click_id']
            except :
                google_ad_click_id = ''
            try:
                hs_arr = dd['properties']['hs_arr']
            except :
                hs_arr = ''
            try:
                hs_campaign = dd['properties']['campaign_name']
            except :
                hs_campaign = ''
            try:
                hs_closed_amount = dd['properties']['hs_closed_amount']
            except :
                hs_closed_amount = ''
            try:
                hs_closed_amount_in_home_currency = dd['properties']['hs_closed_amount_in_home_currency']
            except :
                hs_closed_amount_in_home_currency = ''
            try:
                hs_created_by_user_id = dd['properties']['hs_created_by_user_id']
            except :
                hs_created_by_user_id = ''
            try:
                hs_deal_stage_probability = dd['properties']['hs_deal_stage_probability']
            except :
                hs_deal_stage_probability = ''
            try:
                hs_forecast_amount = dd['properties']['hs_forecast_amount']
            except :
                hs_forecast_amount = ''
            try:
                hs_forecast_probability = dd['properties']['hs_forecast_probability']
            except :
                hs_forecast_probability = ''
            try:
                hs_is_closed = dd['properties']['hs_is_closed']
            except :
                hs_is_closed = ''
            try:
                hs_is_closed_won = dd['properties']['hs_is_closed_won']
            except :
                hs_is_closed_won = ''
            try:
                hs_lastmodifieddate = dd['properties']['hs_lastmodifieddate']
            except :
                hs_lastmodifieddate = ''
            try:
                hs_likelihood_to_close = dd['properties']['hs_likelihood_to_close']
            except :
                hs_likelihood_to_close = ''

            try:
                hs_manual_forecast_category = dd['properties']['hs_manual_forecast_category']
            except :
                hs_manual_forecast_category = ''
            try:
                hs_merged_object_ids = dd['properties']['hs_merged_object_ids']
            except :
                hs_merged_object_ids = ''
            try:
                hs_mrr = dd['properties']['hs_mrr']
            except :
                hs_mrr = ''
            try:
                hs_next_step = dd['properties']['hs_next_step']
            except :
                hs_next_step = ''
            try:
                hs_object_id = dd['properties']['hs_object_id']
            except :
                hs_object_id = ''
            try:
                hs_predicted_amount = dd['properties']['hs_predicted_amount']
            except :
                hs_predicted_amount = ''
            try:
                hs_predicted_amount_in_home_currency = dd['properties']['hs_predicted_amount_in_home_currency']
            except :
                hs_predicted_amount_in_home_currency = ''
            try:
                hs_projected_amount = dd['properties']['hs_projected_amount']
            except :
                hs_projected_amount = ''
            try:
                hs_projected_amount_in_home_currency = dd['properties']['hs_projected_amount_in_home_currency']
            except :
                hs_projected_amount_in_home_currency = ''
            try:
                hs_tcv = dd['properties']['hs_tcv']
            except :
                hs_tcv = ''
            try:
                hs_time_in_appointmentscheduled = dd['properties']['hs_time_in_appointmentscheduled']
            except :
                hs_time_in_appointmentscheduled = ''
            try:
                hs_time_in_closedlost = dd['properties']['hs_time_in_closedlost']
            except :
                hs_time_in_closedlost = ''
            try:
                hs_time_in_closedwon = dd['properties']['hs_time_in_closedwon']
            except :
                hs_time_in_closedwon = ''
            try:
                hs_time_in_contractsent = dd['properties']['hs_time_in_contractsent']
            except :
                hs_time_in_contractsent = ''
            try:
                hs_time_in_decisionmakerboughtin = dd['properties']['hs_time_in_decisionmakerboughtin']
            except :
                hs_time_in_decisionmakerboughtin = ''
            try:
                hs_time_in_presentationscheduled = dd['properties']['hs_time_in_presentationscheduled']
            except :
                hs_time_in_presentationscheduled = ''
            try:
                hs_time_in_qualifiedtobuy = dd['properties']['hs_time_in_qualifiedtobuy']
            except :
                hs_time_in_qualifiedtobuy = ''
            try:
                hs_unique_creation_key = dd['properties']['hs_unique_creation_key']
            except :
                hs_unique_creation_key = ''
            try:
                hs_updated_by_user_id = dd['properties']['hs_updated_by_user_id']
            except :
                hs_updated_by_user_id = ''
            try:
                hs_user_ids_of_all_owners = dd['properties']['hs_user_ids_of_all_owners']
            except :
                hs_user_ids_of_all_owners = ''
            try:
                hubspot_owner_assigneddate = dd['properties']['hubspot_owner_assigneddate']
            except :
                hubspot_owner_assigneddate = ''        
            try:
                application_uuid3 = dd['properties']['application_uuid3']
            except :
                application_uuid3 = ''
            try:
                dealname = dd['properties']['dealname']
            except :
                dealname = ''
            try:
                salesforcelastsynctime = dd['properties']['salesforcelastsynctime']
            except :
                salesforcelastsynctime = ''
            try:
                amount = dd['properties']['amount']
            except :
                amount = ''
            try:
                dealstage = dd['properties']['dealstage']
            except :
                dealstage = ''
            try:
                onboardingfrontlink = dd['properties']['onboardingfrontlink']
            except :
                onboardingfrontlink = ''
            try:
                pipeline = dd['properties']['pipeline']
            except :
                pipeline = ''
            try:
                closedate = dd['properties']['closedate']
            except :
                closedate = ''
            try:
                onboardingadminlink = dd['properties']['onboardingadminlink']
            except :
                onboardingadminlink = ''
            try:
                createdate = dd['properties']['createdate']
            except :
                createdate = ''     
            try:
                hs_latest_meeting_activity = dd['properties']['hs_latest_meeting_activity']
            except :
                hs_latest_meeting_activity = ''
            try:
                hs_sales_email_last_replied = dd['properties']['hs_sales_email_last_replied']
            except :
                hs_sales_email_last_replied = ''
            try:
                hubspot_owner_id = dd['properties']['hubspot_owner_id']
            except :
                hubspot_owner_id = ''
            try:
                notes_last_contacted = dd['properties']['notes_last_contacted']
            except :
                notes_last_contacted = ''
            try:
                notes_last_updated = dd['properties']['notes_last_updated']
            except :
                notes_last_updated = ''
            try:
                notes_next_activity_date = dd['properties']['notes_next_activity_date']
            except :
                notes_next_activity_date = ''
            try:
                num_contacted_notes = dd['properties']['num_contacted_notes']
            except :
                num_contacted_notes = ''
            try:
                num_notes = dd['properties']['num_notes']
            except :
                num_notes = ''
            try:
                hs_createdate = dd['properties']['hs_createdate']
            except :
                hs_createdate = ''
            try:
                hubspot_team_id = dd['properties']['hubspot_team_id']
            except :
                hubspot_team_id = ''
            try:
                dealtype = dd['properties']['dealtype']
            except :
                dealtype = ''
            try:
                hs_all_owner_ids = dd['properties']['hs_all_owner_ids']
            except :
                hs_all_owner_ids = ''
            try:
                description = dd['properties']['description']
                description = description.replace(';','',1000)
            except :
                description = ''
            try:
                hs_all_team_ids = dd['properties']['hs_all_team_ids'].replace(';','',1000)
            except :
                hs_all_team_ids = ''
            try:
                hs_all_accessible_team_ids = dd['properties']['hs_all_accessible_team_ids']
            except :
                hs_all_accessible_team_ids = ''
            try:
                num_associated_contacts = dd['properties']['num_associated_contacts']
            except :
                num_associated_contacts = ''
            try:
                closed_lost_reason = dd['properties']['closed_lost_reason']
            except :
                closed_lost_reason = ''
            try:
                closed_won_reason = dd['properties']['closed_won_reason']
            except :
                closed_won_reason = ''

            deals_all_fields_record.append({
                'id' : id ,
                'amount_in_home_currency' : amount_in_home_currency ,
                'days_to_close' : days_to_close ,
                'hs_acv' : hs_acv ,
                'hs_analytics_source' : hs_analytics_source ,
                'hs_analytics_source_data_1' : hs_analytics_source_data_1 ,
                'hs_analytics_source_data_2' : hs_analytics_source_data_2 ,
                'hs_arr' : hs_arr ,
                'hs_campaign' : hs_campaign ,
                'hs_closed_amount' : hs_closed_amount ,
                'hs_closed_amount_in_home_currency' : hs_closed_amount_in_home_currency ,
                'hs_created_by_user_id' : hs_created_by_user_id ,
                'hs_forecast_amount' : hs_forecast_amount ,
                'hs_forecast_probability' : hs_forecast_probability ,
                'hs_is_closed' : hs_is_closed ,
                'hs_is_closed_won' : hs_is_closed_won ,
                'hs_lastmodifieddate' : hs_lastmodifieddate[:10] ,
                'hs_likelihood_to_close' : hs_likelihood_to_close ,
                'hs_manual_forecast_category' : hs_manual_forecast_category ,
                'hs_merged_object_ids' : hs_merged_object_ids ,
                'hs_mrr' : hs_mrr ,
                'hs_next_step' : hs_next_step ,
                'hs_object_id' : hs_object_id ,
                'hs_predicted_amount' : hs_predicted_amount ,
                'hs_predicted_amount_in_home_currency' : hs_predicted_amount_in_home_currency ,
                'hs_projected_amount' : hs_projected_amount ,
                'hs_projected_amount_in_home_currency' : hs_projected_amount_in_home_currency ,
                'hs_tcv' : hs_tcv ,
                'hs_time_in_appointmentscheduled' : hs_time_in_appointmentscheduled ,
                'hs_time_in_closedlost' : hs_time_in_closedlost ,
                'hs_time_in_closedwon' : hs_time_in_closedwon ,
                'hs_time_in_contractsent' : hs_time_in_contractsent ,
                'hs_time_in_decisionmakerboughtin' : hs_time_in_decisionmakerboughtin ,
                'hs_time_in_presentationscheduled' : hs_time_in_presentationscheduled ,
                'hs_time_in_qualifiedtobuy' : hs_time_in_qualifiedtobuy ,
                'hs_unique_creation_key' : hs_unique_creation_key ,
                'hs_updated_by_user_id' : hs_updated_by_user_id ,
                'hs_user_ids_of_all_owners' : hs_user_ids_of_all_owners ,
                'hubspot_owner_assigneddate' : hubspot_owner_assigneddate ,
                'application_uuid3' : application_uuid3 ,
                'dealname' : dealname ,
                'salesforcelastsynctime' : salesforcelastsynctime ,
                'amount' : amount ,
                'dealstage' : dealstage ,
                'onboardingfrontlink' : onboardingfrontlink ,
                'pipeline' : pipeline ,
                'closedate' : closedate ,
                'onboardingadminlink' : onboardingadminlink ,
                'createdate' : createdate ,
                'hs_latest_meeting_activity' : hs_latest_meeting_activity ,
                'hs_sales_email_last_replied' : hs_sales_email_last_replied ,
                'hubspot_owner_id' : hubspot_owner_id ,
                'notes_last_contacted' : notes_last_contacted ,
                'notes_last_updated' : notes_last_updated ,
                'notes_next_activity_date' : notes_next_activity_date ,
                'num_contacted_notes' : num_contacted_notes ,
                'num_notes' : num_notes ,
                'hs_createdate' : hs_createdate ,
                'hubspot_team_id' : hubspot_team_id ,
                'dealtype' : dealtype ,
                'hs_all_owner_ids' : hs_all_owner_ids ,
                'description' : description ,
                'hs_all_team_ids' : hs_all_team_ids ,
                'hs_all_accessible_team_ids' : hs_all_accessible_team_ids ,
                'num_associated_contacts' : num_associated_contacts ,
                'closed_lost_reason' : closed_lost_reason ,
                'closed_won_reason' : closed_won_reason ,
                'miss_tariffa___motivo_ko' : miss_tariffa___motivo_ko ,
                'miss_tariffa___motivo_trash' : miss_tariffa___motivo_trash ,
                'google_ad_click_id' : google_ad_click_id ,
                'tipo_di_ordine' : tipo_di_ordine 
            })



    deals_all_fields = pd.DataFrame(deals_all_fields_record)


    deals_all_fields['hs_lastmodifieddate'] = pd.to_datetime(deals_all_fields['hs_lastmodifieddate'], format='%Y-%m-%d')

    deals_all_fields = deals_all_fields[(deals_all_fields['hs_lastmodifieddate'] >= start_date)]   

    return deals_all_fields