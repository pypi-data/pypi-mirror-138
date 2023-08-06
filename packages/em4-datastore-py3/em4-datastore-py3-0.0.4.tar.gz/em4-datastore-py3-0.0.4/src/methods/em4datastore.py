# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import google
import mock
import logging
from google.cloud import datastore


def get_db():
    if os.getenv('TESTING', '').startswith('yes'):
        # localhost
        os.environ["DATASTORE_DATASET"] = "test"
        os.environ["DATASTORE_PROJECT_ID"] = "test"
        os.environ["DATASTORE_EMULATOR_HOST"] = "localhost:8001"
        os.environ["DATASTORE_EMULATOR_HOST_PATH"] = "localhost:8001/datastore"
        os.environ["DATASTORE_HOST"] = "http://localhost:8001"

        credentials = mock.Mock(spec=google.auth.credentials.Credentials)
        # db = ndb.Client(project="test", credentials=credentials)
        db = datastore.Client()
    else:
        db = datastore.Client()

    return db


class Em4DataStore:

    def __init__(self):
        self.client = get_db()

    def allocateId4Entity(self, entity_name):
        keys = self.client.allocate_ids(self.client.key(entity_name), 1)
        return keys[0].id

    def basic_query(self, entitykind, field, value, operator):
        # [START datastore_basic_query]
        query = self.client.query(kind=entitykind)
        query.add_filter(field, operator, value)
        # query.add_filter("priority", ">=", 4)
        # query.order = ["-email"]
        # [END datastore_basic_query]

        return list(query.fetch())

    def delete(self, entitykind, id):
        # [START datastore_delete]
        key = self.client.key(entitykind, id)
        self.client.delete(key)
        # [END datastore_delete]

        return key

    def insertClient(self, name, lastname, phone, email, address1, address2, city, state, zipcode):
        # client = get_db()
        # return 'Hello World!.22...'
        key = self.client.key("ClientInformation")
        entity = datastore.Entity(key)

        entity.update(name=name, lastname=lastname, phone=phone, email=email,
                      address1=address1, address2=address2, city=city,
                      state=state, zipcode=zipcode)
        self.client.put(entity)
        c1_id = entity.id

        logging.info('client created {}'.format(c1_id))
        message = str('ClientInformation has been inserted with ID :{}'.format(c1_id))

        return message, c1_id

    def upsertClient(self, name, lastname, phone, email, address1, address2, city, state, zipcode, namedKey=None):
        key = self.client.key("ClientInformation", email)
        entity = self.client.get(key)
        elist = self.basic_query("ClientInformation", "email", email, "=")
        if len(elist) == 0:
            # if entity is None:
            entity = datastore.Entity(self.client.key("ClientInformation"))

            entity.update(name=name, lastname=lastname, phone=phone, email=email,
                          address1=address1, address2=address2, city=city,
                          state=state, zipcode=zipcode)
            self.client.put(entity)
            c1_id = entity.id
            logging.info('client created {}'.format(c1_id))
        else:
            entity = elist[0]
            # delete("ClientInformation", email)
            self.updateClient(id=entity.id, name=name, lastname=lastname, phone=phone, email=email,
                              address1=address1, address2=address2, city=city,
                              state=state, zipcode=zipcode)
            logging.info('client has been updated {}'.format(entity.id))
        message = str('upsert: ClientInformation has been inserted with ID :{}'.format(entity.id))

        return message, entity.id

    def updateClient(self,
                     id=None,
                     name=None,
                     lastname=None,
                     phone=None,
                     email=None,
                     address1=None,
                     address2=None,
                     city=None,
                     state=None,
                     zipcode=None):
        with self.client.transaction():
            if id is not None:
                key = self.client.key("ClientInformation", id)
                task = self.client.get(key)
                task["name"] = name
                task["lastname"] = lastname
                task["phone"] = phone
                task["email"] = email
                task["address1"] = address1
                task["address2"] = address2
                task["city"] = city
                task["state"] = state
                task["zipcode"] = zipcode
                self.client.put(task)

        # [END datastore_update]

        return task

    def insertUserAuthInformation(self, username, password, client_id):
        key = self.client.key("UserAuthInformation")
        entity = datastore.Entity(key)
        entity.update(username=username, password=password, client_id=client_id)

        self.client.put(entity)
        c1_id = entity.id

        logging.info('UserAuthInformation created {}'.format(c1_id))
        message = str('UserAuthInformation has been inserted for {} with ID :{}'.format(username, c1_id))

        return message

    def updateUserAuthInformation(self, id=None, username=None, password=None, client_id=None):
        with self.client.transaction():
            if id is not None:
                key = self.client.key("UserAuthInformation", id)
                task = self.client.get(key)
                task["username"] = username
                task["password"] = password
                task["client_id"] = client_id
                self.client.put(task)
        # [END datastore_update]

        return task

    def upsertUserAuthInformation(self, username, password, client_id, namedkey=None):

        elist = self.basic_query("UserAuthInformation", "username", username, "=")
        if len(elist) == 0:
            # if entity is None:
            entity = datastore.Entity(self.client.key("UserAuthInformation"))

            entity.update(username=username, password=password, client_id=client_id)
            self.client.put(entity)
            c1_id = entity.id
            logging.info('client created {}'.format(c1_id))
        else:
            entity = elist[0]
            # delete("ClientInformation", email)
            self.updateUserAuthInformation(id=entity.id, username=username, password=password, client_id=client_id)
            logging.info('UserAuthInformation has been updated {}'.format(entity.id))
        message = str('upsert: UserAuthInformation has been inserted with ID :{}'.format(entity.id))

        return message, entity.id

    def insertInsuranceInformation(self, insurance_company, naic, policy, expiry, client_id):
        key = self.client.key("InsuranceInformation")
        entity = datastore.Entity(key)
        entity.update(insurance_company=insurance_company,
                      naic=naic,
                      policy=policy,
                      expiry=expiry,
                      client_id=client_id)

        self.client.put(entity)
        c1_id = entity.id

        logging.info('InsuranceInformation created {}'.format(c1_id))
        message = str('InsuranceInformation has been inserted ID :{}'.format(c1_id))
        return message

    def updateInsuranceInformation(self, id=None, insurance_company=None, naic=None, policy=None, expiry=None,
                                   client_id=None):
        with self.client.transaction():
            if id is not None:
                key = self.client.key("InsuranceInformation", id)
                task = self.client.get(key)
                task["insurance_company"] = insurance_company
                task["naic"] = naic
                task["policy"] = policy
                task["expiry"] = expiry
                task["client_id"] = client_id
                self.client.put(task)
        # [END datastore_update]

        return task

    def upsertInsuranceInformation(self, insurance_company=None, naic=None, policy=None, expiry=None, client_id=None):

        elist = self.basic_query("InsuranceInformation", "insurance_company", insurance_company, "=")
        if len(elist) == 0:
            # if entity is None:
            entity = datastore.Entity(self.client.key("InsuranceInformation"))

            entity.update(insurance_company=insurance_company,
                          naic=naic,
                          policy=policy,
                          expiry=expiry,
                          client_id=client_id)
            self.client.put(entity)
            c1_id = entity.id
            logging.info('InsuranceInformation created {}'.format(c1_id))
        else:
            entity = elist[0]
            # delete("ClientInformation", email)
            self.updateInsuranceInformation(id=entity.id,
                                            insurance_company=insurance_company,
                                            naic=naic,
                                            policy=policy,
                                            expiry=expiry,
                                            client_id=client_id)
            logging.info('InsuranceInformation has been updated {}'.format(entity.id))
        message = str('upsert: InsuranceInformation has been inserted with ID :{}'.format(entity.id))

        return message, entity.id

    def insertLastRunDate(self, process_id, last_run_date):
        key = self.client.key("LastRunDate")
        entity = datastore.Entity(key)
        entity.update(process_id=process_id, last_run_date=last_run_date)
        self.client.put(entity)
        c1_id = entity.id

        logging.info('LastRunDate created {}'.format(c1_id))
        message = str('LastRunDate for {} has been inserted with :{}'.format(process_id, last_run_date))
        return message

    def updateLastRunDate(self, id=None, process_id=None, last_run_date=None):
        with self.client.transaction():
            if id is not None:
                key = self.client.key("LastRunDate", id)
                task = self.client.get(key)
                task["process_id"] = process_id
                task["last_run_date"] = last_run_date
                self.client.put(task)
        # [END datastore_update]

        return task

    def upsertLastRunDate(self, id=None, process_id=None, last_run_date=None):

        elist = self.basic_query("LastRunDate", "process_id", process_id, "=")
        if len(elist) == 0:
            # if entity is None:
            entity = datastore.Entity(self.client.key("LastRunDate"))

            entity.update(process_id=process_id, last_run_date=last_run_date)
            self.client.put(entity)
            c1_id = entity.id
            logging.info('LastRunDate created {}'.format(c1_id))
        else:
            entity = elist[0]
            # delete("ClientInformation", email)
            self.updateLastRunDate(id=entity.id, process_id=process_id, last_run_date=last_run_date)
            logging.info('LastRunDate has been updated {}'.format(entity.id))
        message = str('upsert: LastRunDate has been inserted with ID :{}'.format(entity.id))

        return message, entity.id

    def insertVehicleInformation(self,
                                 client_id,
                                 ftp_id,
                                 tenant_id,
                                 imei,
                                 department,
                                 vin,
                                 license_plate,
                                 start_date,
                                 make,
                                 model,
                                 year,
                                 vehicle_id,
                                 odometer,
                                 ecm_expiry_date,
                                 activity_date,
                                 software,
                                 latest_activity_date,
                                 tested,
                                 comments,
                                 date_added,
                                 user_id):
        key = self.client.key("VehicleInformation")
        entity = datastore.Entity(key)
        entity.update(client_id=client_id,
                      ftp_id=ftp_id,
                      tenant_id=tenant_id,
                      imei=imei,
                      department=department,
                      vin=vin,
                      license_plate=license_plate,
                      start_date=start_date,
                      make=make,
                      model=model,
                      year=year,
                      vehicle_id=vehicle_id,
                      odometer=odometer,
                      ecm_expiry_date=ecm_expiry_date,
                      activity_date=activity_date,
                      software=software,
                      latest_activity_date=latest_activity_date,
                      tested=tested,
                      comments=comments,
                      date_added=date_added,
                      user_id=user_id)
        self.client.put(entity)
        c1_id = entity.id
        logging.info('VehicleInformation created {}'.format(c1_id))
        message = str('VehicleInformation for vehicle {} has been inserted with ID:{}'.format(vehicle_id, c1_id))
        return message

    def upsertVehicleInformation(self,
                                 client_id=None,
                                 ftp_id=None,
                                 tenant_id=None,
                                 imei=None,
                                 department=None,
                                 vin=None,
                                 license_plate=None,
                                 start_date=None,
                                 make=None,
                                 model=None,
                                 year=None,
                                 vehicle_id=None,
                                 odometer=None,
                                 ecm_expiry_date=None,
                                 activity_date=None,
                                 software=None,
                                 latest_activity_date=None,
                                 tested=None,
                                 comments=None,
                                 date_added=None,
                                 user_id=None):

        elist = self.basic_query("VehicleInformation", "vin", vin, "=")
        if len(elist) == 0:
            # if entity is None:
            entity = datastore.Entity(self.client.key("VehicleInformation"))

            entity.update(client_id=client_id,
                          ftp_id=ftp_id,
                          tenant_id=tenant_id,
                          imei=imei,
                          department=department,
                          vin=vin,
                          license_plate=license_plate,
                          start_date=start_date,
                          make=make,
                          model=model,
                          year=year,
                          vehicle_id=vehicle_id,
                          odometer=odometer,
                          ecm_expiry_date=ecm_expiry_date,
                          activity_date=activity_date,
                          software=software,
                          latest_activity_date=latest_activity_date,
                          tested=tested,
                          comments=comments,
                          date_added=date_added,
                          user_id=user_id)
            self.client.put(entity)
            c1_id = entity.id
            logging.info('ClientInformation created {}'.format(c1_id))
        else:
            entity = elist[0]
            # delete("ClientInformation", email)
            self.updateVehicleInformation(id=entity.id,
                                          client_id=client_id,
                                          ftp_id=ftp_id,
                                          tenant_id=tenant_id,
                                          imei=imei,
                                          department=department,
                                          vin=vin,
                                          license_plate=license_plate,
                                          start_date=start_date,
                                          make=make,
                                          model=model,
                                          year=year,
                                          vehicle_id=vehicle_id,
                                          odometer=odometer,
                                          ecm_expiry_date=ecm_expiry_date,
                                          activity_date=activity_date,
                                          software=software,
                                          latest_activity_date=latest_activity_date,
                                          tested=tested,
                                          comments=comments,
                                          date_added=date_added,
                                          user_id=user_id)
            logging.info('ClientInformation has been updated {}'.format(entity.id))
        message = str('upsert: ClientInformation has been inserted with ID :{}'.format(entity.id))

        return message, entity.id

    def updateVehicleInformation(self,
                                 id=None,
                                 client_id=None,
                                 ftp_id=None,
                                 tenant_id=None,
                                 imei=None,
                                 department=None,
                                 vin=None,
                                 license_plate=None,
                                 start_date=None,
                                 make=None,
                                 model=None,
                                 year=None,
                                 vehicle_id=None,
                                 odometer=None,
                                 ecm_expiry_date=None,
                                 activity_date=None,
                                 software=None,
                                 latest_activity_date=None,
                                 tested=None,
                                 comments=None,
                                 date_added=None,
                                 user_id=None):

        with self.client.transaction():
            if id is not None:
                key = self.client.key("VehicleInformation", id)
                task = self.client.get(key)
                task["client_id"] = client_id
                task["ftp_id"] = ftp_id
                task["tenant_id"] = tenant_id
                task["imei"] = imei
                task["department"] = department
                task["vin"] = vin
                task["license_plate"] = license_plate
                task["start_date"] = start_date
                task["make"] = make
                task["model"] = model
                task["year"] = year
                task["vehicle_id"] = vehicle_id
                task["odometer"] = odometer
                task["ecm_expiry_date"] = ecm_expiry_date
                task["activity_date"] = activity_date
                task["software"] = software
                task["latest_activity_date"] = latest_activity_date
                task["tested"] = tested
                task["comments"] = comments
                task["date_added"] = date_added
                task["user_id"] = user_id
                self.client.put(task)
        # [END datastore_update]

        return task

    def insertStickerInformation(self, sticker, expiry, ftp_id, client_id):
        key = self.client.key("StickerInformation")
        entity = datastore.Entity(key)
        entity.update(sticker=sticker, expiry=expiry, ftp_id=ftp_id, client_id=client_id)
        self.client.put(entity)
        c1_id = entity.id

        logging.info('StickerInformation created {}'.format(c1_id))
        message = str('StickerInformation for sticker {} has been inserted with :{}'.format(sticker, c1_id))
        return message

    def updateStickerInformation(self, id=None, sticker=None, expiry=None, ftp_id=None, client_id=None):
        with self.client.transaction():
            if id is not None:
                key = self.client.key("StickerInformation", id)
                task = self.client.get(key)
                task["sticker"] = sticker
                task["expiry"] = expiry
                task["ftp_id"] = ftp_id
                task["client_id"] = client_id
                self.client.put(task)
        # [END datastore_update]

        return task

    def upsertStickerInformation(self, sticker=None, expiry=None, ftp_id=None, client_id=None):

        elist = self.basic_query("StickerInformation", "sticker", sticker, "=")
        if len(elist) == 0:
            # if entity is None:
            entity = datastore.Entity(self.client.key("StickerInformation"))

            entity.update(sticker=sticker, expiry=expiry, ftp_id=ftp_id, client_id=client_id)
            self.client.put(entity)
            c1_id = entity.id
            logging.info('StickerInformation created {}'.format(c1_id))
        else:
            entity = elist[0]
            # delete("ClientInformation", email)
            self.updateStickerInformation(id=entity.id,
                                          sticker=sticker,
                                          expiry=expiry,
                                          ftp_id=ftp_id,
                                          client_id=client_id)
            logging.info('StickerInformation has been updated {}'.format(entity.id))
        message = str('upsert: StickerInformation has been inserted with ID :{}'.format(entity.id))

        return message, entity.id

    def insertEmCarsDailyRpt(
            self,
            res_sys_no_obd,
            lic_st_id,
            ets_id,
            etnj2_sw_ver,
            vin,
            vin_src,
            vehicle_vin,
            vehicle_vin_src,
            obd2_vin_obd,
            vin_mask,
            lic_no_obd,
            lic_jur_obd,
            lic_src,
            model_yr_obd,
            make_obd,
            model_obd,
            gvwr,
            no_of_cyl,
            eng_size,
            trans_type,
            fuel_cd,
            vid_sys_no,
            curr_odo_rdng_obd,
            prev_odo_rdng_obd,
            mvc_reg_code,
            mvc_vehicle_type_code,
            test_type,
            start_time_obd,
            end_time_obd,
            create_date_obd,
            prev_test_date,
            emiss_test_type,
            primary_emiss_test_code,
            bulb_check_res,
            chk_eng_light_on_obd,
            indicator_light_result,
            exempt_from_obd,
            obd_bypassed,
            bypass_obd_allowed,
            obd2_connect_res,
            communic_res,
            obd,
            obd2_test_fl,
            pcm_mudule_id,
            obd_module_id_2,
            obd_module_id_3,
            obd_type,
            obd_calid,
            obd_cvn,
            cvn_exclusion,
            pid_count_obd,
            obd_pid00_obd,
            obd_pid20_obd,
            obd_pid40_obd,
            obd_rpm_obd,
            rpm_exclusion,
            misfire_mon_res_obd,
            fuel_sys_mon_res_obd,
            comp_cmpnt_res_obd,
            catalyst_mon_res_obd,
            heat_cat_mon_res_obd,
            evap_sys_mon_res_obd,
            sec_air_sys_mon_res_obd,
            air_cond_mon_res_obd,
            oxy_sens_mon_res_obd,
            htd_oxy_sns_mon_res_obd,
            egr_sys_mon_res_obd,
            rdy_mon_obd,
            tot_unset_rdy_mon,
            readiness_status,
            continuous_monit_xclusion,
            exempt_from_readiness,
            mil_command_stat,
            dtc1_obd,
            dtc2_obd,
            dtc3_obd,
            dtc4_obd,
            dtc5_obd,
            dtc6_obd,
            dtc7_obd,
            dtc8_obd,
            dtc9_obd,
            dtc10_obd,
            tot_stored_dtcs_obd,
            catalyst_dtc_pres_obd,
            pend_dtc1_obd,
            pend_dtc2_obd,
            pend_dtc3_obd,
            pend_dtc4_obd,
            pend_dtc5_obd,
            pend_dtc6_obd,
            pend_dtc7_obd,
            pend_dtc8_obd,
            pend_dtc9_obd,
            pend_dtc10_obd,
            cat_retest_exclusion,
            obd_warmups_obd,
            obd_code_cleared_distance_obd,
            obd_mil_on_distance_obd,
            obd_code_cleared_time_obd,
            obd_mil_on_time_obd,
            emiss_clarification,
            misc_comnt,
            misc_comnt_res,
            misc_emiss_reject_comment,
            misc_emiss_reject_result,
            overall_tamper_result,
            ex_sys_res,
            overall_obd2_res,
            exh_emiss_test_res,
            overall_gas_cap_res,
            ovr_exh_obd2_em_res,
            overall_emiss_res,
            overall_saf_res,
            overall_test_res,
            created_date_sys,
            created_user_sys,
            update_date_sys,
            update_user_sys
    ):
        key = self.client.key("EmCarsDailyRpt")
        entity = datastore.Entity(key)
        entity.update(res_sys_no_obd=res_sys_no_obd,
                      lic_st_id=lic_st_id,
                      ets_id=ets_id,
                      etnj2_sw_ver=etnj2_sw_ver,
                      vin=vin,
                      vin_src=vin_src,
                      vehicle_vin=vehicle_vin,
                      vehicle_vin_src=vehicle_vin_src,
                      obd2_vin_obd=obd2_vin_obd,
                      vin_mask=vin_mask,
                      lic_no_obd=lic_no_obd,
                      lic_jur_obd=lic_jur_obd,
                      lic_src=lic_src,
                      model_yr_obd=model_yr_obd,
                      make_obd=make_obd,
                      model_obd=model_obd,
                      gvwr=gvwr,
                      no_of_cyl=no_of_cyl,
                      eng_size=eng_size,
                      trans_type=trans_type,
                      fuel_cd=fuel_cd,
                      vid_sys_no=vid_sys_no,
                      curr_odo_rdng_obd=curr_odo_rdng_obd,
                      prev_odo_rdng_obd=prev_odo_rdng_obd,
                      mvc_reg_code=mvc_reg_code,
                      mvc_vehicle_type_code=mvc_vehicle_type_code,
                      test_type=test_type,
                      start_time_obd=start_time_obd,
                      end_time_obd=end_time_obd,
                      create_date_obd=create_date_obd,
                      prev_test_date=prev_test_date,
                      emiss_test_type=emiss_test_type,
                      primary_emiss_test_code=primary_emiss_test_code,
                      bulb_check_res=bulb_check_res,
                      chk_eng_light_on_obd=chk_eng_light_on_obd,
                      indicator_light_result=indicator_light_result,
                      exempt_from_obd=exempt_from_obd,
                      obd_bypassed=obd_bypassed,
                      bypass_obd_allowed=bypass_obd_allowed,
                      obd2_connect_res=obd2_connect_res,
                      communic_res=communic_res,
                      obd=obd,
                      obd2_test_fl=obd2_test_fl,
                      pcm_mudule_id=pcm_mudule_id,
                      obd_module_id_2=obd_module_id_2,
                      obd_module_id_3=obd_module_id_3,
                      obd_type=obd_type,
                      obd_calid=obd_calid,
                      obd_cvn=obd_cvn,
                      cvn_exclusion=cvn_exclusion,
                      pid_count_obd=pid_count_obd,
                      obd_pid00_obd=obd_pid00_obd,
                      obd_pid20_obd=obd_pid20_obd,
                      obd_pid40_obd=obd_pid40_obd,
                      obd_rpm_obd=obd_rpm_obd,
                      rpm_exclusion=rpm_exclusion,
                      misfire_mon_res_obd=misfire_mon_res_obd,
                      fuel_sys_mon_res_obd=fuel_sys_mon_res_obd,
                      comp_cmpnt_res_obd=comp_cmpnt_res_obd,
                      catalyst_mon_res_obd=catalyst_mon_res_obd,
                      heat_cat_mon_res_obd=heat_cat_mon_res_obd,
                      evap_sys_mon_res_obd=evap_sys_mon_res_obd,
                      sec_air_sys_mon_res_obd=sec_air_sys_mon_res_obd,
                      air_cond_mon_res_obd=air_cond_mon_res_obd,
                      oxy_sens_mon_res_obd=oxy_sens_mon_res_obd,
                      htd_oxy_sns_mon_res_obd=htd_oxy_sns_mon_res_obd,
                      egr_sys_mon_res_obd=egr_sys_mon_res_obd,
                      rdy_mon_obd=rdy_mon_obd,
                      tot_unset_rdy_mon=tot_unset_rdy_mon,
                      readiness_status=readiness_status,
                      continuous_monit_xclusion=continuous_monit_xclusion,
                      exempt_from_readiness=exempt_from_readiness,
                      mil_command_stat=mil_command_stat,
                      dtc1_obd=dtc1_obd,
                      dtc2_obd=dtc2_obd,
                      dtc3_obd=dtc3_obd,
                      dtc4_obd=dtc4_obd,
                      dtc5_obd=dtc5_obd,
                      dtc6_obd=dtc6_obd,
                      dtc7_obd=dtc7_obd,
                      dtc8_obd=dtc8_obd,
                      dtc9_obd=dtc9_obd,
                      dtc10_obd=dtc10_obd,
                      tot_stored_dtcs_obd=tot_stored_dtcs_obd,
                      catalyst_dtc_pres_obd=catalyst_dtc_pres_obd,
                      pend_dtc1_obd=pend_dtc1_obd,
                      pend_dtc2_obd=pend_dtc2_obd,
                      pend_dtc3_obd=pend_dtc3_obd,
                      pend_dtc4_obd=pend_dtc4_obd,
                      pend_dtc5_obd=pend_dtc5_obd,
                      pend_dtc6_obd=pend_dtc6_obd,
                      pend_dtc7_obd=pend_dtc7_obd,
                      pend_dtc8_obd=pend_dtc8_obd,
                      pend_dtc9_obd=pend_dtc9_obd,
                      pend_dtc10_obd=pend_dtc10_obd,
                      cat_retest_exclusion=cat_retest_exclusion,
                      obd_warmups_obd=obd_warmups_obd,
                      obd_code_cleared_distance_obd=obd_code_cleared_distance_obd,
                      obd_mil_on_distance_obd=obd_mil_on_distance_obd,
                      obd_code_cleared_time_obd=obd_code_cleared_time_obd,
                      obd_mil_on_time_obd=obd_mil_on_time_obd,
                      emiss_clarification=emiss_clarification,
                      misc_comnt=misc_comnt,
                      misc_comnt_res=misc_comnt_res,
                      misc_emiss_reject_comment=misc_emiss_reject_comment,
                      misc_emiss_reject_result=misc_emiss_reject_result,
                      overall_tamper_result=overall_tamper_result,
                      ex_sys_res=ex_sys_res,
                      overall_obd2_res=overall_obd2_res,
                      exh_emiss_test_res=exh_emiss_test_res,
                      overall_gas_cap_res=overall_gas_cap_res,
                      ovr_exh_obd2_em_res=ovr_exh_obd2_em_res,
                      overall_emiss_res=overall_emiss_res,
                      overall_saf_res=overall_saf_res,
                      overall_test_res=overall_test_res,
                      created_date_sys=created_date_sys,
                      created_user_sys=created_user_sys,
                      update_date_sys=update_date_sys,
                      update_user_sys=update_user_sys)
        self.client.put(entity)
        c1_id = entity.id

        logging.info('EmCarsDailyRpt created {}'.format(c1_id))
        message = str('EmCarsDailyRpt for vin {} has been inserted with :{}'.format(vehicle_vin, c1_id))
        return message

    def updateEmCarsDailyRpt(
            self,
            id=None,
            res_sys_no_obd=None,
            lic_st_id=None,
            ets_id=None,
            etnj2_sw_ver=None,
            vin=None,
            vin_src=None,
            vehicle_vin=None,
            vehicle_vin_src=None,
            obd2_vin_obd=None,
            vin_mask=None,
            lic_no_obd=None,
            lic_jur_obd=None,
            lic_src=None,
            model_yr_obd=None,
            make_obd=None,
            model_obd=None,
            gvwr=None,
            no_of_cyl=None,
            eng_size=None,
            trans_type=None,
            fuel_cd=None,
            vid_sys_no=None,
            curr_odo_rdng_obd=None,
            prev_odo_rdng_obd=None,
            mvc_reg_code=None,
            mvc_vehicle_type_code=None,
            test_type=None,
            start_time_obd=None,
            end_time_obd=None,
            create_date_obd=None,
            prev_test_date=None,
            emiss_test_type=None,
            primary_emiss_test_code=None,
            bulb_check_res=None,
            chk_eng_light_on_obd=None,
            indicator_light_result=None,
            exempt_from_obd=None,
            obd_bypassed=None,
            bypass_obd_allowed=None,
            obd2_connect_res=None,
            communic_res=None,
            obd=None,
            obd2_test_fl=None,
            pcm_mudule_id=None,
            obd_module_id_2=None,
            obd_module_id_3=None,
            obd_type=None,
            obd_calid=None,
            obd_cvn=None,
            cvn_exclusion=None,
            pid_count_obd=None,
            obd_pid00_obd=None,
            obd_pid20_obd=None,
            obd_pid40_obd=None,
            obd_rpm_obd=None,
            rpm_exclusion=None,
            misfire_mon_res_obd=None,
            fuel_sys_mon_res_obd=None,
            comp_cmpnt_res_obd=None,
            catalyst_mon_res_obd=None,
            heat_cat_mon_res_obd=None,
            evap_sys_mon_res_obd=None,
            sec_air_sys_mon_res_obd=None,
            air_cond_mon_res_obd=None,
            oxy_sens_mon_res_obd=None,
            htd_oxy_sns_mon_res_obd=None,
            egr_sys_mon_res_obd=None,
            rdy_mon_obd=None,
            tot_unset_rdy_mon=None,
            readiness_status=None,
            continuous_monit_xclusion=None,
            exempt_from_readiness=None,
            mil_command_stat=None,
            dtc1_obd=None,
            dtc2_obd=None,
            dtc3_obd=None,
            dtc4_obd=None,
            dtc5_obd=None,
            dtc6_obd=None,
            dtc7_obd=None,
            dtc8_obd=None,
            dtc9_obd=None,
            dtc10_obd=None,
            tot_stored_dtcs_obd=None,
            catalyst_dtc_pres_obd=None,
            pend_dtc1_obd=None,
            pend_dtc2_obd=None,
            pend_dtc3_obd=None,
            pend_dtc4_obd=None,
            pend_dtc5_obd=None,
            pend_dtc6_obd=None,
            pend_dtc7_obd=None,
            pend_dtc8_obd=None,
            pend_dtc9_obd=None,
            pend_dtc10_obd=None,
            cat_retest_exclusion=None,
            obd_warmups_obd=None,
            obd_code_cleared_distance_obd=None,
            obd_mil_on_distance_obd=None,
            obd_code_cleared_time_obd=None,
            obd_mil_on_time_obd=None,
            emiss_clarification=None,
            misc_comnt=None,
            misc_comnt_res=None,
            misc_emiss_reject_comment=None,
            misc_emiss_reject_result=None,
            overall_tamper_result=None,
            ex_sys_res=None,
            overall_obd2_res=None,
            exh_emiss_test_res=None,
            overall_gas_cap_res=None,
            ovr_exh_obd2_em_res=None,
            overall_emiss_res=None,
            overall_saf_res=None,
            overall_test_res=None,
            created_date_sys=None,
            created_user_sys=None,
            update_date_sys=None,
            update_user_sys=None):
        with self.client.transaction():
            if id is not None:
                key = self.client.key("EmCarsDailyRpt", id)
                task = self.client.get(key)
                task["res_sys_no_obd"] = res_sys_no_obd
                task["lic_st_id"] = lic_st_id
                task["ets_id"] = ets_id
                task["etnj2_sw_ver"] = etnj2_sw_ver
                task["vin"] = vin
                task["vin_src"] = vin_src
                task["vehicle_vin"] = vehicle_vin
                task["vehicle_vin_src"] = vehicle_vin_src
                task["obd2_vin_obd"] = obd2_vin_obd
                task["vin_mask"] = vin_mask
                task["lic_no_obd"] = lic_no_obd
                task["lic_jur_obd"] = lic_jur_obd
                task["lic_src"] = lic_src
                task["model_yr_obd"] = model_yr_obd
                task["make_obd"] = make_obd
                task["model_obd"] = model_obd
                task["gvwr"] = gvwr
                task["no_of_cyl"] = no_of_cyl
                task["eng_size"] = eng_size
                task["trans_type"] = trans_type
                task["fuel_cd"] = fuel_cd
                task["vid_sys_no"] = vid_sys_no
                task["curr_odo_rdng_obd"] = curr_odo_rdng_obd
                task["prev_odo_rdng_obd"] = prev_odo_rdng_obd
                task["mvc_reg_code"] = mvc_reg_code
                task["mvc_vehicle_type_code"] = mvc_vehicle_type_code
                task["test_type"] = test_type
                task["start_time_obd"] = start_time_obd
                task["end_time_obd"] = end_time_obd
                task["create_date_obd"] = create_date_obd
                task["prev_test_date"] = prev_test_date
                task["emiss_test_type"] = emiss_test_type
                task["primary_emiss_test_code"] = primary_emiss_test_code
                task["bulb_check_res"] = bulb_check_res
                task["chk_eng_light_on_obd"] = chk_eng_light_on_obd
                task["indicator_light_result"] = indicator_light_result
                task["exempt_from_obd"] = exempt_from_obd
                task["obd_bypassed"] = obd_bypassed
                task["bypass_obd_allowed"] = bypass_obd_allowed
                task["obd2_connect_res"] = obd2_connect_res
                task["communic_res"] = communic_res
                task["obd"] = obd
                task["obd2_test_fl"] = obd2_test_fl
                task["pcm_mudule_id"] = pcm_mudule_id
                task["obd_module_id_2"] = obd_module_id_2
                task["obd_module_id_3"] = obd_module_id_3
                task["obd_type"] = obd_type
                task["obd_calid"] = obd_calid
                task["obd_cvn"] = obd_cvn
                task["cvn_exclusion"] = cvn_exclusion
                task["pid_count_obd"] = pid_count_obd
                task["obd_pid00_obd"] = obd_pid00_obd
                task["obd_pid20_obd"] = obd_pid20_obd
                task["obd_pid40_obd"] = obd_pid40_obd
                task["obd_rpm_obd"] = obd_rpm_obd
                task["rpm_exclusion"] = rpm_exclusion
                task["misfire_mon_res_obd"] = misfire_mon_res_obd
                task["fuel_sys_mon_res_obd"] = fuel_sys_mon_res_obd
                task["comp_cmpnt_res_obd"] = comp_cmpnt_res_obd
                task["catalyst_mon_res_obd"] = catalyst_mon_res_obd
                task["heat_cat_mon_res_obd"] = heat_cat_mon_res_obd
                task["evap_sys_mon_res_obd"] = evap_sys_mon_res_obd
                task["sec_air_sys_mon_res_obd"] = sec_air_sys_mon_res_obd
                task["air_cond_mon_res_obd"] = air_cond_mon_res_obd
                task["oxy_sens_mon_res_obd"] = oxy_sens_mon_res_obd
                task["htd_oxy_sns_mon_res_obd"] = htd_oxy_sns_mon_res_obd
                task["egr_sys_mon_res_obd"] = egr_sys_mon_res_obd
                task["rdy_mon_obd"] = rdy_mon_obd
                task["tot_unset_rdy_mon"] = tot_unset_rdy_mon
                task["readiness_status"] = readiness_status
                task["continuous_monit_xclusion"] = continuous_monit_xclusion
                task["exempt_from_readiness"] = exempt_from_readiness
                task["mil_command_stat"] = mil_command_stat
                task["dtc1_obd"] = dtc1_obd
                task["dtc2_obd"] = dtc2_obd
                task["dtc3_obd"] = dtc3_obd
                task["dtc4_obd"] = dtc4_obd
                task["dtc5_obd"] = dtc5_obd
                task["dtc6_obd"] = dtc6_obd
                task["dtc7_obd"] = dtc7_obd
                task["dtc8_obd"] = dtc8_obd
                task["dtc9_obd"] = dtc9_obd
                task["dtc10_obd"] = dtc10_obd
                task["tot_stored_dtcs_obd"] = tot_stored_dtcs_obd
                task["catalyst_dtc_pres_obd"] = catalyst_dtc_pres_obd
                task["pend_dtc1_obd"] = pend_dtc1_obd
                task["pend_dtc2_obd"] = pend_dtc2_obd
                task["pend_dtc3_obd"] = pend_dtc3_obd
                task["pend_dtc4_obd"] = pend_dtc4_obd
                task["pend_dtc5_obd"] = pend_dtc5_obd
                task["pend_dtc6_obd"] = pend_dtc6_obd
                task["pend_dtc7_obd"] = pend_dtc7_obd
                task["pend_dtc8_obd"] = pend_dtc8_obd
                task["pend_dtc9_obd"] = pend_dtc9_obd
                task["pend_dtc10_obd"] = pend_dtc10_obd
                task["cat_retest_exclusion"] = cat_retest_exclusion
                task["obd_warmups_obd"] = obd_warmups_obd
                task["obd_code_cleared_distance_obd"] = obd_code_cleared_distance_obd
                task["obd_mil_on_distance_obd"] = obd_mil_on_distance_obd
                task["obd_code_cleared_time_obd"] = obd_code_cleared_time_obd
                task["obd_mil_on_time_obd"] = obd_mil_on_time_obd
                task["emiss_clarification"] = emiss_clarification
                task["misc_comnt"] = misc_comnt
                task["misc_comnt_res"] = misc_comnt_res
                task["misc_emiss_reject_comment"] = misc_emiss_reject_comment
                task["misc_emiss_reject_result"] = misc_emiss_reject_result
                task["overall_tamper_result"] = overall_tamper_result
                task["ex_sys_res"] = ex_sys_res
                task["overall_obd2_res"] = overall_obd2_res
                task["exh_emiss_test_res"] = exh_emiss_test_res
                task["overall_gas_cap_res"] = overall_gas_cap_res
                task["ovr_exh_obd2_em_res"] = ovr_exh_obd2_em_res
                task["overall_emiss_res"] = overall_emiss_res
                task["overall_saf_res"] = overall_saf_res
                task["overall_test_res"] = overall_test_res
                task["created_date_sys"] = created_date_sys
                task["created_user_sys"] = created_user_sys
                task["update_date_sys"] = update_date_sys
                task["update_user_sys"] = update_user_sys
                self.client.put(task)
        # [END datastore_update]

        return task
