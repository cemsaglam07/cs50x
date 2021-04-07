-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Theft took place on July 28, 2020 and that it took place on Chamberlin Street.
-- cat log.sql | sqlite3 fiftyville.db > output.txt

-- Find out the report's description, given the location and time of the theft:
SELECT id, description FROM crime_scene_reports WHERE year = 2020 AND month = 07 AND day = 28 AND street = "Chamberlin Street";

-- Key takeaways:
-- Report ID: 295
-- Stolen items: CS50 duck
-- Time: July 28, 2020 10:15am
-- Location: Chamberlin Street courthouse
-- Interviews with three present witnesses

-- Find the interviews of the three witnesses:
SELECT id, name, transcript FROM interviews WHERE year = 2020 AND month = 07 AND day = 28;

-- Key takeaways:
-- Ruth (161):      Parking lot within 10 mins
-- Eugene (162):    ATM on Fifer Street in the morning
-- Raymond (163):   When leaving, called sb for <1min
--                  Tomorrow, earliest flight
--                  Reciever should purchase ticket

-- Refine logs from 10:15 to 10:25 (+/- 10 mins) as per Ruth's testimony
SELECT id, hour, minute, activity, license_plate FROM courthouse_security_logs
WHERE year = 2020 AND month = 07 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25;

-- Not much is found, but we can check for matching people later on.
-- Here are the suspicious license plates:
-- id  | HH | MM | actv | plates
-- 260 | 10 | 16 | exit | 5P2BI95
-- 261 | 10 | 18 | exit | 94KL13X
-- 262 | 10 | 18 | exit | 6P58WS2
-- 263 | 10 | 19 | exit | 4328GD8
-- 264 | 10 | 20 | exit | G412CB7
-- 265 | 10 | 21 | exit | L93JTIZ
-- 266 | 10 | 23 | exit | 322W7JE
-- 267 | 10 | 23 | exit | 0NTHK55

-- Check for people who were at the ATM on Fifer Street in the morning as per Eugene's testimony:
SELECT id, account_number, transaction_type, amount FROM atm_transactions
WHERE year = 2020 AND month = 07 AND day = 28 AND atm_location = "Fifer Street";

-- Again, here are the results, finding intersections will be useful:
-- id  | account  | type     | $$
-- 246 | 28500762 | withdraw | 48
-- 264 | 28296815 | withdraw | 20
-- 266 | 76054385 | withdraw | 60
-- 267 | 49610011 | withdraw | 50
-- 269 | 16153065 | withdraw | 80
-- 275 | 86363979 | deposit  | 10  (not this one, for sure)
-- 288 | 25506511 | withdraw | 20
-- 313 | 81061156 | withdraw | 30
-- 336 | 26013199 | withdraw | 35

-- Check for phone records under 1 mins:
SELECT id, caller, receiver, duration FROM phone_calls
WHERE year = 2020 AND month = 07 AND day = 28 AND duration <= 60;

-- Results:
-- id  | caller         | reciever       | duration
-- 221 | (130) 555-0289 | (996) 555-8899 | 51
-- 224 | (499) 555-9472 | (892) 555-8872 | 36
-- 233 | (367) 555-5533 | (375) 555-8161 | 45
-- 234 | (609) 555-5876 | (389) 555-5198 | 60
-- 251 | (499) 555-9472 | (717) 555-1342 | 50
-- 254 | (286) 555-6063 | (676) 555-6554 | 43
-- 255 | (770) 555-1861 | (725) 555-3243 | 49
-- 261 | (031) 555-6622 | (910) 555-3251 | 38
-- 279 | (826) 555-1652 | (066) 555-9701 | 55
-- 281 | (338) 555-6650 | (704) 555-2131 | 54

-- Now let's find the earliest flight and its passengers. There's a few steps to this.
SELECT id, hour, minute, origin_airport_id, destination_airport_id FROM flights
WHERE year = 2020 AND month = 07 AND day = 29 AND origin_airport_id IN (
SELECT id FROM airports WHERE city = "Fiftyville");

-- The earliest flight is at 8:20 to destination_id = 4 with flight_id = 36
-- id | hour | minute | origin_airport_id | destination_airport_id
-- 18 | 16 | 0 | 8 | 6
-- 23 | 12 | 15 | 8 | 11
-- 36 | 8 | 20 | 8 | 4
-- 43 | 9 | 30 | 8 | 1
-- 53 | 15 | 20 | 8 | 9

-- Now let's find the passengers:
SELECT id, name, phone_number, passport_number, license_plate FROM people WHERE passport_number IN(
SELECT passport_number FROM passengers WHERE flight_id = 36);

-- id     | name  | phone number   | passports  | plates
-- 395717 | Bobby | (826) 555-1652 | 9878712108 | 30G67EN
-- 398010 | Roger | (130) 555-0289 | 1695452385 | G412CB7
-- 449774 | Madison | (286) 555-6063 | 1988161715 | 1106N58
-- 467400 | Danielle | (389) 555-5198 | 8496433585 | 4328GD8
-- 560886 | Evelyn | (499) 555-9472 | 8294398571 | 0NTHK55
-- 651714 | Edward | (328) 555-1152 | 1540955065 | 130LD9Z
-- 686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X
-- 953679 | Doris | (066) 555-9701 | 7214083635 | M51FA04

-- Ultimately, let's find the matching people:
SELECT id, name, phone_number, passport_number, license_plate FROM people
-- The first parameter will look for courthouse security logs
WHERE license_plate IN(SELECT license_plate FROM courthouse_security_logs
WHERE year = 2020 AND month = 07 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25)
-- The second parameter will look for the passengers list
AND passport_number IN(SELECT passport_number FROM passengers WHERE flight_id = 36)
-- The third parameter will look for phone records
AND phone_number IN(SELECT caller FROM phone_calls
WHERE year = 2020 AND month = 07 AND day = 28 AND duration <= 60)
-- The fourth parameter will look for ATM records:
AND id IN(SELECT person_id FROM bank_accounts WHERE account_number IN(
SELECT account_number FROM atm_transactions WHERE year = 2020 AND month = 07 AND day = 28
AND atm_location = "Fifer Street" AND transaction_type = "withdraw"));

-- The result is only one person -- the thief:
-- id     | name   | phone number   | passport   | plates
-- 686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X

-- Now let's see who Ernest (the thief) called:
SELECT id, name, phone_number, passport_number, license_plate FROM people
WHERE phone_number IN (SELECT receiver FROM phone_calls
WHERE year = 2020 AND month = 07 AND day = 28 AND duration <= 60
AND caller = (SELECT phone_number FROM people WHERE id = 686048));

-- Ernest escaped to:
SELECT city FROM airports WHERE id = 4;