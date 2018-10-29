from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import datetime
import pyxlsb
import difflib
import sys

data = {}

wb = pyxlsb.open_workbook(sys.argv[1])
with wb.get_sheet('Profile') as sheet:
	for row in sheet.rows():
		if list(row[0])[2] != None and list(row[0])[2].strip().lower().replace(':', '') == 'address':
			data['address'] = list(row[1])[2]

with wb.get_sheet('InsuranceQuote') as sheet:
	for row in sheet.rows():
		if list(row[0])[2] != None:
			data[list(row[0])[2].strip().lower().replace(':', '')] = list(row[1])[2]


options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
driver.get('https://myquote.acorninsure.com/ProductSelect.aspx?r=false&brand=Site')

# Home Page
# =======================================================
select = Select(driver.find_element_by_id('UserType'))
select.select_by_value('getaquote')

select = Select(driver.find_element_by_id('Products'))
select.select_by_value('Taxi')

# ========================================================
driver.find_element_by_id('MainContent_btnNext').click()
# ========================================================

# Qualification Page
# ========================================================
driver.find_element_by_id('MainContent_btnNext').click()
# ========================================================

# About You Page
# ======================================================================================================================
title = Select(driver.find_element_by_id('MainContent_CUSTOMER_INSURED_PARTY__TITLE_ID__1'))
if data['title'].lower() == 'mrs':
	title_value = '004'
elif data['title'].lower() == 'miss':
	title_value = '002'
elif data['title'].lower() == 'ms':
	title_value = '005'
elif 'doctor' in data['title'].lower():
	if 'male' in data['title'].lower():
		title_value = '001'
	else:
		title_value = '123'
else:
	title_value = '003'
title.select_by_value(title_value)


first_name = driver.find_element_by_id("MainContent_CUSTOMER_INSURED_PARTY__FORENAME__1")
first_name_text = data['first name']
first_name.send_keys(first_name_text)

surname = driver.find_element_by_id("MainContent_CUSTOMER_INSURED_PARTY__SURNAME__1")
surname_text = data['surname']
surname.send_keys(surname_text)

email = driver.find_element_by_id("CUSTOMER_INSURED_PARTY__EMAIL__1")
email_text = data['email']
email.send_keys(email_text)

re_email = driver.find_element_by_id("txtRetypeEmail")
re_email.send_keys(email_text)

phone = driver.find_element_by_id("MainContent_txtTelephoneMobile")
phone_text = data['best contact number']
phone.send_keys(phone_text)

postcode = driver.find_element_by_id("MainContent_CUSTOMER_CLIENT_ADDRESS__POSTCODE__1")
postcode_text = data['postcode']
postcode.send_keys(postcode_text)
driver.find_element_by_id('MainContent_btnCUSTOMER_CLIENT_ADDRESS__POSTCODE__1').click()

driver.implicitly_wait(21)

address = Select(driver.find_element_by_id('MainContent_ddlCUSTOMER_CLIENT_ADDRESS__POSTCODE__1'))
address_text = difflib.get_close_matches(data['address'], driver.find_element_by_id('MainContent_ddlCUSTOMER_CLIENT_ADDRESS__POSTCODE__1').text.split('\n'), 1, (0.1))
address_text_temp = address_text[0]
colon_count = 0
for item in address_text[0]:
	if item == ',':
		colon_count = colon_count + 1
		colons = ''
		while len(colons) < colon_count:
			colons = colons + ':'
		address_text_temp = address_text_temp.replace(',', colons, 1)
address_text[0] = address_text_temp.strip()
address.select_by_value(address_text[0])

date_of_birth = datetime.datetime.utcfromtimestamp((data['date of birth'] - 25569) * 86400.0)
dob_date = driver.find_element_by_id("MainContent_CUSTOMER_INSURED_PARTY__DOB__1__dd")
dob_date_text = date_of_birth.day
dob_date.send_keys(dob_date_text)
dob_month = driver.find_element_by_id("MainContent_CUSTOMER_INSURED_PARTY__DOB__1__mm")
dob_month_text = date_of_birth.month
dob_month.send_keys(dob_month_text)
dob_year = driver.find_element_by_id("MainContent_CUSTOMER_INSURED_PARTY__DOB__1__yy")
dob_year_text = date_of_birth.year
dob_year.send_keys(dob_year_text)

marital_status = Select(driver.find_element_by_id('CUSTOMER_INSURED_PARTY__MARITAL_STATUS_ID__1'))
if data['martial status'].lower() == 'divorced':
	marital_status_value = 'D'
elif 'married' in data['martial status'].lower():
	if 'common' in data['martial status'].lower():
		marital_status_value = 'C'
	else:
		marital_status_value = 'M'
elif data['martial status'].lower() == 'not applicable':
	marital_status_value = 'N'
elif 'partnered' in data['martial status'].lower():
	if 'civil' in data['martial status'].lower():
		marital_status_value = 'B'
	else:
		marital_status_value = 'P'
elif data['martial status'].lower() == 'separated':
	marital_status_value = 'A'
elif data['martial status'].lower() == 'widowed':
	marital_status_value = 'W'
else:
	marital_status_value = 'S'
marital_status.select_by_value(marital_status_value) 

if data['do you know the vehicle registration'].lower() == 'no':
	print('Functionality not implemented yet due to deficiency of data')
	# driver.find_element_by_css_selector("span[id='rblDoYouKnowVehicleRegistration'] label[for='rblDoYouKnowVehicleRegistration_1']").click()
else:

	driver.find_element_by_css_selector("span[id='rblDoYouKnowVehicleRegistration'] label[for='rblDoYouKnowVehicleRegistration_0']").click()

vehicle_registartion = driver.find_element_by_id("CUSTOMER_VEHICLE__REGN_NUMBER__1")
vehicle_registartion_text = data['registration number']
vehicle_registartion.send_keys(vehicle_registartion_text)

driver.implicitly_wait(21)

driver.find_element_by_id("MainContent_btnVehicle").click()

driver.find_element_by_id("ddlVehicles").click()
driver.find_element_by_css_selector('div[id="MainContent_upVehicle"] div[id="MainContent_vehiclesearchresult"] select option:not([selected])').click()

if data['is this the correct vehicle'].lower() == 'no':
	print('Functionality not implemented yet due to deficiency of data')
	# driver.find_element_by_css_selector("span[id='correctVeh'] label[for='correctVeh_1']").click()
else:
	driver.find_element_by_css_selector("span[id='correctVeh'] label[for='correctVeh_0']").click()

value = driver.find_element_by_id('CUSTOMER_VEHICLE__VALUE_DESC__1')
value_text = str(data['value'])
value.send_keys(value_text)

date_of_vehicle_purchase = datetime.datetime.utcfromtimestamp((data['date purchased'] - 25569) * 86400.0)
vehicle_purchase_date = driver.find_element_by_id('MainContent_CUSTOMER_VEHICLE__PURCHASE__1__dd')
vehicle_purchase_date_text = date_of_vehicle_purchase.day
vehicle_purchase_date.send_keys(vehicle_purchase_date_text)
vehicle_purchase_month = driver.find_element_by_id('MainContent_CUSTOMER_VEHICLE__PURCHASE__1__mm')
vehicle_purchase_month_text = date_of_vehicle_purchase.month
vehicle_purchase_month.send_keys(vehicle_purchase_month_text)
vehicle_purchase_year = driver.find_element_by_id('MainContent_CUSTOMER_VEHICLE__PURCHASE__1__yy')
vehicle_purchase_year_text = date_of_vehicle_purchase.year
vehicle_purchase_year.send_keys(vehicle_purchase_year_text)

if data['imported'].lower() == 'yes':
	print('Functionality not implemented yet due to deficiency of data')
	# driver.find_element_by_css_selector("span[id='MainContent_CUSTOMER_VEHICLE__IMPORTEDCAR__1'] label[for='MainContent_CUSTOMER_VEHICLE__IMPORTEDCAR__1_0']").click()
else:
	driver.find_element_by_css_selector("span[id='MainContent_CUSTOMER_VEHICLE__IMPORTEDCAR__1'] label[for='MainContent_CUSTOMER_VEHICLE__IMPORTEDCAR__1_1']").click()

if data['left hand drive'].lower() == 'yes':
	driver.find_element_by_css_selector("span[id='MainContent_CUSTOMER_VEHICLE__LEFTHANDYN__1'] label[for='MainContent_CUSTOMER_VEHICLE__LEFTHANDYN__1_0']").click()
else:
	driver.find_element_by_css_selector("span[id='MainContent_CUSTOMER_VEHICLE__LEFTHANDYN__1'] label[for='MainContent_CUSTOMER_VEHICLE__LEFTHANDYN__1_1']").click()

# Not Implemented Due to deficiency of data in the excel sheet; this field do not exist
# +++++++++++++++++++++++++++++++++++++++++ 
# if data['security devices'].lower() == 'yes':
# 	driver.find_element_by_css_selector("span[id='MainContent_rblHasAdditionalSecurity'] label[for='MainContent_rblHasAdditionalSecurity_0']").click() 
# else:
# 	driver.find_element_by_css_selector("span[id='MainContent_rblHasAdditionalSecurity'] label[for='MainContent_rblHasAdditionalSecurity_1']").click() 
driver.find_element_by_css_selector("span[id='MainContent_rblHasAdditionalSecurity'] label[for='MainContent_rblHasAdditionalSecurity_1']").click() 
# Default
# +++++++++++++++++++++++++++++++++++++++++


ownership = Select(driver.find_element_by_id('MainContent_CUSTOMER_VEHICLE__OWNERSHIP_ID__1'))
if '12 month' in data['ownership'].lower():
	ownership_value = '3T41GF25'
elif data['ownership'].lower() == 'credit hire':
	ownership_value = '3T41GHQ4'
elif data['ownership'].lower() == 'proposer/policyholder':
	ownership_value = '1'
elif data['ownership'].lower() == 'short term rental':
	ownership_value = '3T41GGQ0'
elif data['ownership'].lower() == 'spouse':
	ownership_value = '2'
else:
	ownership_value = '9'
ownership.select_by_value(ownership_value)

if data['parking overnight'].lower() == 'at home':
	driver.find_element_by_css_selector("span[id='MainContent_divparkingovernight_ID'] label[for='MainContent_divparkingovernight_ID_0']").click()
elif data['parking overnight'].lower() == 'drive':
	driver.find_element_by_css_selector("span[id='MainContent_divparkingovernight_ID'] label[for='MainContent_divparkingovernight_ID_1']").click()
elif data['parking overnight'].lower() == 'secure garage':
	driver.find_element_by_css_selector("span[id='MainContent_divparkingovernight_ID'] label[for='MainContent_divparkingovernight_ID_2']").click()
elif data['parking overnight'].lower() == 'public car park':
	driver.find_element_by_css_selector("span[id='MainContent_divparkingovernight_ID'] label[for='MainContent_divparkingovernight_ID_3']").click()
elif data['parking overnight'].lower() == 'secure car park':
	driver.find_element_by_css_selector("span[id='MainContent_divparkingovernight_ID'] label[for='MainContent_divparkingovernight_ID_4']").click()
else:
	driver.find_element_by_css_selector("span[id='MainContent_divparkingovernight_ID'] label[for='MainContent_divparkingovernight_ID_5']").click()

ownership = Select(driver.find_element_by_id('MainContent_CUSTOMER_CV__TAXI_AREA_ID__1'))
ownership.select_by_visible_text(data['operating area'])

operating_postcode = driver.find_element_by_id("MainContent_CUSTOMER_CV__OPERATINGPOSTCODE__1")
operating_postcode_text = data['postcode']
operating_postcode.send_keys(operating_postcode_text)

time.sleep(5)

# ======================================================================================================================
driver.find_element_by_id('MainContent_btnNext').click()
# ======================================================================================================================

# Vehicle Cover
# ======================================================================================================================
required_cover = Select(driver.find_element_by_id('MainContent_CUSTOMER_MOTOR__VEHICLE_COVER_ID__1'))
if data['what cover is required'].lower() == 'comprehensive':
	required_cover.select_by_value('01')
	voluntary_access = Select(driver.find_element_by_id('MainContent_CUSTOMER_EXCESS__EXCESSAMOUNT__1'))
	voluntary_access_value = str(int(data['voluntary excess']/50))
	if voluntary_access_value == '0':
		voluntary_access_value = '00'
	voluntary_access.select_by_value(voluntary_access_value)
elif 'only' in data['what cover is required'].lower():
	required_cover.select_by_value('03')
else:
	required_cover.select_by_value('02')
	voluntary_access = Select(driver.find_element_by_id('MainContent_CUSTOMER_EXCESS__EXCESSAMOUNT__1'))
	voluntary_access.select_by_value(str(data['voluntary excess']/50))

no_claim_discount = driver.find_element_by_id('CUSTOMER_MOTOR__NOCLAIMSBONUS__1')
no_claim_discount_text = str(int(data['how many years of no claim bonus']))
no_claim_discount.send_keys(no_claim_discount_text)

reason = Select(driver.find_element_by_id('CUSTOMER_NCD__VEHICLE_NCD_REASON_ID__1'))
reason_text = difflib.get_close_matches(data['reason'], driver.find_element_by_id('CUSTOMER_NCD__VEHICLE_NCD_REASON_ID__1').text.split('\n'), 1)
if reason_text[0].strip().lower() == 'Claim Outstanding'.lower():
	reason.select_by_value('1')
elif reason_text[0] == 'Claim Settled'.lower():
	reason.select_by_value('2')
elif reason_text[0] == 'Company Car'.lower():
	reason.select_by_value('3')
elif reason_text[0] == 'Commercial Policy'.lower():
	reason.select_by_value('4')
elif reason_text[0] == 'Mobility Policy'.lower():
	reason.select_by_value('5')
elif reason_text[0] == 'No Previous Insurance'.lower():
	reason.select_by_value('6')
elif reason_text[0] == 'Policy Not in Force for Whole Year'.lower():
	reason.select_by_value('7')
elif reason_text[0] == 'Previous Bonus Expired'.lower():
	reason.select_by_value('8')
elif reason_text[0] == 'Second Vehicle'.lower():
	reason.select_by_value('9')
else:
	reason.select_by_value('10')

# ======================================================================================================================
driver.find_element_by_id('MainContent_btnNext').click()
# ======================================================================================================================

# Driver Details
# ======================================================================================================================
UK_residency_years = driver.find_element_by_id('CUSTOMER_INSURED_PARTY__UK_RESIDENCE_YEARS__1')
UK_residency_years_text = str(int(data['number of years of uk residency']))
UK_residency_years.send_keys(UK_residency_years_text)

if data['main driver'].lower() == 'no':
	driver.find_element_by_css_selector("span[id='MainContent_CUSTOMER_POLICY_LINK__MAINUSERYN__1'] label[for='MainContent_CUSTOMER_POLICY_LINK__MAINUSERYN__1_1']").click()
else:
	driver.find_element_by_css_selector("span[id='MainContent_CUSTOMER_POLICY_LINK__MAINUSERYN__1'] label[for='MainContent_CUSTOMER_POLICY_LINK__MAINUSERYN__1_0']").click()

if 'domestic' in data['vehicle use'].lower():
	driver.find_element_by_css_selector("span[id='MainContent_CUSTOMER_VEHICLE__VEHICLE_USE_ID__1'] label[for='MainContent_CUSTOMER_VEHICLE__VEHICLE_USE_ID__1_2']").click()
elif 'public' in data['vehicle use'].lower():
	driver.find_element_by_css_selector("span[id='MainContent_CUSTOMER_VEHICLE__VEHICLE_USE_ID__1'] label[for='MainContent_CUSTOMER_VEHICLE__VEHICLE_USE_ID__1_1']").click()
else:
	driver.find_element_by_css_selector("span[id='MainContent_CUSTOMER_VEHICLE__VEHICLE_USE_ID__1'] label[for='MainContent_CUSTOMER_VEHICLE__VEHICLE_USE_ID__1_0']").click()

if data['is your main occupation taxi driver?'].lower() == 'no':
	print('Functionality not implemented yet due to deficiency of data')
	# driver.find_element_by_css_selector("span[id='MainContent_rbtTaxiOccupation'] label[for='MainContent_rbtTaxiOccupation_1']").click()
else:
	driver.find_element_by_css_selector("span[id='MainContent_rbtTaxiOccupation'] label[for='MainContent_rbtTaxiOccupation_0']").click()

driving_license_number = driver.find_element_by_id('CUSTOMER_DRIVER_DETAILS__DRIVING_LICENCE_NO__1')
driving_license_number_text = data['driving license number']
driving_license_number.send_keys(driving_license_number_text)

license_type = Select(driver.find_element_by_id('MainContent_CUSTOMER_POLICY_LINK__LICENSE_TYPE_ID__1'))
license_type_value = difflib.get_close_matches(data['license type'], driver.find_element_by_id('MainContent_CUSTOMER_POLICY_LINK__LICENSE_TYPE_ID__1').text.split('\n'), 1)
if 'Foreign'.lower() in license_type_value[0].strip().lower():
	license_type.select_by_value('I')
elif 'EEC Licence'.lower() in license_type_value[0].strip().lower():
	license_type.select_by_value('E')
elif 'Non-EU'.lower() in license_type_value[0].strip().lower():
	license_type.select_by_value('H')
elif 'Full UK'.lower() in license_type_value[0].strip().lower():
	license_type.select_by_value('F')
elif 'International'.lower() in license_type_value[0].strip().lower():
	license_type.select_by_value('N')
elif 'Other'.lower() in license_type_value[0].strip().lower():
	license_type.select_by_value('Z')
elif 'Provisional (UK)'.lower() in license_type_value[0].strip().lower():
	license_type.select_by_value('P')
elif 'HGV Licence'.lower() in license_type_value[0].strip().lower():
	license_type.select_by_value('9')
else:
	license_type.select_by_value('Q')

license_date = datetime.datetime.utcfromtimestamp((data['date current license obtained'] - 25569) * 86400.0)
license_obtain_date = driver.find_element_by_id('MainContent_CUSTOMER_POLICY_LINK__DATEPASSED__1__dd')
license_obtain_date_text = license_date.day
license_obtain_date.send_keys(license_obtain_date_text)
license_obtain_month = driver.find_element_by_id('MainContent_CUSTOMER_POLICY_LINK__DATEPASSED__1__mm')
license_obtain_month_text = license_date.month
license_obtain_month.send_keys(license_obtain_month_text)
license_obtain_year = driver.find_element_by_id('MainContent_CUSTOMER_POLICY_LINK__DATEPASSED__1__yy')
license_obtain_year_text = license_date.year
license_obtain_year.send_keys(license_obtain_year_text)

if data['any motoring convictions'].lower() == 'yes':
	print('Functionality not implemented yet due to deficiency of data')
	# driver.find_element_by_css_selector("span[id='MainContent_rdlAnyMotoringConvictions'] label[for='MainContent_rdlAnyMotoringConvictions_0']").click()
else:
	driver.find_element_by_css_selector("span[id='MainContent_rdlAnyMotoringConvictions'] label[for='MainContent_rdlAnyMotoringConvictions_1']").click()

if data['any previous motor claims lat 5 years?'].lower() == 'yes':
	print('Functionality not implemented yet due to deficiency of data')
	# driver.find_element_by_css_selector("span[id='MainContent_rdlAnyMotorClaims'] label[for='MainContent_rdlAnyMotorClaims_0']").click()
else:
	driver.find_element_by_css_selector("span[id='MainContent_rdlAnyMotorClaims'] label[for='MainContent_rdlAnyMotorClaims_1']").click()

if data['any medical condition?'].lower() == 'yes':
	print('Functionality not implemented yet due to deficiency of data')
	# driver.find_element_by_css_selector("span[id='MainContent_rdlAnyMedicalConditions'] label[for='MainContent_rdlAnyMedicalConditions_0']").click()
else:
	driver.find_element_by_css_selector("span[id='MainContent_rdlAnyMedicalConditions'] label[for='MainContent_rdlAnyMedicalConditions_1']").click()

if data['ever convicted for criminal offence?'].lower() == 'yes':
	driver.find_element_by_css_selector("span[id='MainContent_CUSTOMER_INSURED_PARTY__CRIMINAL_OFFENCEYN__1'] label[for='MainContent_CUSTOMER_INSURED_PARTY__CRIMINAL_OFFENCEYN__1_0']").click()
else:
	driver.find_element_by_css_selector("span[id='MainContent_CUSTOMER_INSURED_PARTY__CRIMINAL_OFFENCEYN__1'] label[for='MainContent_CUSTOMER_INSURED_PARTY__CRIMINAL_OFFENCEYN__1_1']").click()

if data['ever been refused cover?'].lower() == 'yes':
	driver.find_element_by_css_selector("span[id='MainContent_CUSTOMER_INSURED_PARTY__REFUSEDYN__1'] label[for='MainContent_CUSTOMER_INSURED_PARTY__REFUSEDYN__1_0']").click()
else:
	driver.find_element_by_css_selector("span[id='MainContent_CUSTOMER_INSURED_PARTY__REFUSEDYN__1'] label[for='MainContent_CUSTOMER_INSURED_PARTY__REFUSEDYN__1_1']").click()

if data['everhad terms applied?'].lower() == 'yes':
	driver.find_element_by_css_selector("span[id='MainContent_CUSTOMER_POLICY_LINK__TERMSAPPLIED__1'] label[for='MainContent_CUSTOMER_POLICY_LINK__TERMSAPPLIED__1_0']").click()
else:
	driver.find_element_by_css_selector("span[id='MainContent_CUSTOMER_POLICY_LINK__TERMSAPPLIED__1'] label[for='MainContent_CUSTOMER_POLICY_LINK__TERMSAPPLIED__1_1']").click()

taxi_experience = driver.find_element_by_id('MainContent_CUSTOMER_DRIVER_DETAILS__YEARS_MINIBUS_EXPERIENCE__1')
taxi_experience_text = str(int(data['taxi experience']))
taxi_experience.send_keys(taxi_experience_text)

council_licensed_by = Select(driver.find_element_by_id('MainContent_CUSTOMER_INSURED_PARTY__TAXI_COUNCIL_LICENSE_ID__1'))
council_licensed_by.select_by_visible_text(data['council licenced by'])

driver_option_required = Select(driver.find_element_by_id('MainContent_CUSTOMER_MOTOR__DRIVER_OPTION_ID__1'))
driver_option_required_value = difflib.get_close_matches(data['driver option'], driver.find_element_by_id('MainContent_CUSTOMER_MOTOR__DRIVER_OPTION_ID__1').text.split('\n'), 1)
if driver_option_required_value[0].strip().lower() == 'Insured And 1 Named Driver'.lower():
	driver_option_required.select_by_value('5')
if driver_option_required_value[0].strip().lower() == 'Insured And 2 Named Drivers'.lower():
	driver_option_required.select_by_value('B')
if driver_option_required_value[0].strip().lower() == 'Insured Only'.lower():
	driver_option_required.select_by_value('1')
if driver_option_required_value[0].strip().lower() == 'Named Drivers Excluding Proposer'.lower():
	driver_option_required.select_by_value('3')
if driver_option_required_value[0].strip().lower() == 'One Named Driver Excluding Proposer'.lower():
	driver_option_required.select_by_value('6')

# ======================================================================================================================
driver.find_element_by_id('MainContent_btnNext').click()
# ======================================================================================================================

# (Pre Quote) Your Quote
# ===============================================================================================
current_date = datetime.datetime.now() + datetime.timedelta(hours=1)

cover_start_day = driver.find_element_by_id('MainContent_CUSTOMER_POLICY_DETAILS__POLICYSTARTDATE__1__dd')
cover_start_day.clear()
cover_start_day.send_keys(current_date.day)

cover_start_month = driver.find_element_by_id('MainContent_CUSTOMER_POLICY_DETAILS__POLICYSTARTDATE__1__mm')
cover_start_month.clear()
cover_start_month.send_keys(current_date.month)

cover_start_year = driver.find_element_by_id('MainContent_CUSTOMER_POLICY_DETAILS__POLICYSTARTDATE__1__yy')
cover_start_year.clear()
cover_start_year.send_keys(current_date.year)

cover_start_hour = driver.find_element_by_id('CUSTOMER_POLICY_DETAILS__POLICYSTARTDATE__1__hh')
cover_start_hour.clear()
cover_start_hour.send_keys(current_date.hour)

cover_start_min = driver.find_element_by_id('CUSTOMER_POLICY_DETAILS__POLICYSTARTDATE__1__min')
cover_start_min.clear()
cover_start_min.send_keys(current_date.minute)

# ===============================================================================================
driver.find_element_by_id('btnNext').click()
# ===============================================================================================

# Your Quote
# ===============================================================================================
time.sleep(7)
your_quotes = driver.find_elements_by_css_selector('table[summary="Quotations"] td.col2')
for item in your_quotes:
	print(item.text)