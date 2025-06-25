# M3205_KozlovNS


# Функциональные требования

Выбранная предметная область: [booking](https://www.booking.com/)

## Гости/Клиенты
### 1. Регистрация
* Ввод личных данных: ФИО, адрес электронной почты, номер телефона
* Создание логина и пароля
* Возможность редактировать профиль
### 2. Авторизация
* Вход в систему по логину и паролю
### 3. Выбор отеля
* Фильтрация по городу, датам заезда/выезда, количеству гостей, ценовому диапазону, рейтингу, типу номера
* Просмотр описания, фотографий, оценок
* Проверка доступности на выбранные даты
### 3. Создание бранирование
* Выбор конкретного отеля и номера в нем
* Указание дат заезда/выезда, количества гостей
* Если пользователь зарегистрирован, то его личные данные заполняются автоматичеки
* Если пользователь не зарегистрирован, то ему предлагается зарегистрироваться(без этого невозможно сделать бранирование)
* Возможность выбрать дополнительные услуги
* Стоимость выбранных доп. услуг, добавляется к общей стоимости
* Возможность оплаты части суммы бонусами, при учавстовании пользователя в бонусной программе
* Выбор варианта оплаты (полная, частичная, по прибытии)
### 4. Оплата бронироания
* Если выбрана полная или частичная опалта:
    * Переход на сервис по оплате
* При успехе пометка бронирования как оплачено
* Если выбрана опата по прибытии, то оплат не происходит
### 5. Подтеверждение бронирование
* Генерация и отправка клиенту уникального кода/номера бронирования на указанную контактную почту
### 4. Управление бронированиями
* Просмотр истории бронирований
* Изменение параметров будущих бронирований
* Отмена бронирования
### 5.	Отзывы и рейтинги   
* Возможность поставить только оценку, без написания тектстового отзыва
* Возможность оставлять текстовый отзыв после проживания
* Просмотр собственных отзывов, редактирование

## Аккаунт партнера сервиса(не связвн с аккаунтом обычного пользователя)
### 1. Регистрация
* Ввод личных данных: ФИО, адрес электронной почты, номер телефона
* Создание логина и пароля
* Возможность редактировать профиль
### 2. Авторизация
* Вход в систему по логину и паролю
### 3. Управление отелями
* Добавление новых отелей (название, адрес, город, контакты, описание)
* Редактирование существующих отелей
* Удаление отелей
### 4. Управление номерами
* Добавление новых номеров, указание параметров(тип, вместимость, цена, статус) при добавлении.
* Редактирование информации о существующих номерах (тип, вместимость, цена, статус)
* Возможность добавлять скидки и сезонные предложения на номера
* Контроль статуса номеров (доступен, на ремонте, забронирован)
### 5. Дополнительные услуги
#### Добавление новой услуги
* Указание стоимости услуги
* Указание описания услуги
#### Уже добаленные услуги
* Хранение списка доступных услуг
* Удаление услуги
* Измененеие стоимости услуги
* Измененеие описания услуги


## Бонусная программа, предоствляется сервисом для всех
### 1. Регистрация в программе лояльности (по желанию пользователя)
* Гости могут присоединиться к программе, получая уникальный бонусный счёт
### 2. Начисление бонусов
* Автоматически за оплаченные бронирования
* Возможны отдельные персональные акции для клиентов
### 3. Списание бонусов
* Гость может оплатить часть бронирования баллами
### 4. Просмотр баланса и истории транзакций
* Отображение доступных бонусов
* Отображение всех операций начисления/списания


# Составим ER диаграмму
```plantuml
entity "User" {
  * user_id : serial
  name : varchar(255)
  email : varchar(255)
  phone : varchar(255)
  login : varchar(255)
  bonus_account_id : int <<FK>>
}

entity "Partner" {
  * partner_id : serial
  name : varchar(255)
  email : varchar(255)
  phone : varchar(255)
  login : varchar(255)
  partner_type_id : int <<FK>>
}

entity "Hotel" {
  * hotel_id : serial
  partner_id : int <<FK>>
  hotel_name : varchar(255)
  rating : int
  address : varchar(255)
  city : varchar(255)
  contacts : varchar(255)
  description : varchar(255)
}

entity "Room" {
  * room_id : serial
  hotel_id : int <<FK>>
  description : varchar(255)
  room_type : varchar(255)
  capacity : int
  price : decimal
}

entity "Additional_service" {
  * service_id : serial
  service_name : varchar(255)
  service_description : varchar(255)
  price : decimal
}

entity "Booking" {
  * booking_id : serial
  user_id : int <<FK>>
  room_id : int <<FK>>
  payment_id : int <<FK>>
  check_in_date : date
  check_out_date : date
  guests_number : int
  status : enum
  price : decimal
  date_creation : date
  paid : enum
}

entity "Review" {
  * review_id : serial
  user_id : int <<FK>>
  hotel_id : int <<FK>>
  comment_text : text
  date_creation : date
}

entity "Bonus_Account" {
  * bonus_account_id : serial
  user_id : int <<FK>>
  transaction_id : int <<FK>>
}

entity "Booking_Additional_service" {
  booking_id : int <<FK>>
  service_id : int <<FK>>
}

entity "Payment" {
  * payment_id : serial
  booking_id : int <<FK>>
  payment_date : date
  amount : decimal
  payment_method_id : int <<FK>> ' Заменили строковое поле на FK
  payment_status : enum
}

entity "Bonus_Transaction" {
  * transaction_id : serial
  bonus_account_id : int <<FK>>
  transaction_date : date
  amount : decimal
  transaction_type : varchar(255)
}

entity "PartnerType" {
  * partner_type_id : serial
  type_name : varchar(255)
  description : varchar(255)
}

entity "Amenity" {
  * amenity_id : serial
  amenity_name : varchar(255)
  amenity_description : varchar(255)
}

entity "HotelAmenity" {
  hotel_id : int <<FK>>
  amenity_id : int <<FK>>
}

entity "RoomFacility" {
  * facility_id : serial
  facility_name : varchar(255)
  facility_description : varchar(255)
}

entity "RoomHasFacility" {
  room_id : int <<FK>>
  facility_id : int <<FK>>
}

entity "PaymentMethod" {
  * payment_method_id : serial
  method_name : varchar(255)
}

entity "BookingStatusHistory" {
  * booking_status_history_id : serial
  booking_id : int <<FK>>
  old_status : enum
  new_status : enum
  changed_at : date
}

entity "UserPaymentMethod" {
  * user_payment_method_id : serial
  user_id : int <<FK>>
  payment_method_id : int <<FK>>
  details : varchar(255)
}

"User" ||--o{ "Booking"
"Partner" ||--o{ "Hotel"
"Hotel" ||--o{ "Room"
"Room" ||--o{ "Booking"
"User" ||--o{ "Review"
"Hotel" ||--o{ "Review"
"User" ||--o| "Bonus_Account"
"Booking" ||--|| "Booking_Additional_service"
"Additional_service" ||--|| "Booking_Additional_service"
"Booking" ||--o{ "Payment"
"Bonus_Account" ||--o{ "Bonus_Transaction"

"PartnerType" ||--o{ "Partner"
"Amenity" ||--o{ "HotelAmenity"
"Hotel"   ||--o{ "HotelAmenity"
"RoomFacility" ||--o{ "RoomHasFacility"
"Room"         ||--o{ "RoomHasFacility"
"PaymentMethod" ||--o{ "Payment"
"Booking" ||--o{ "BookingStatusHistory"
"User"          ||--o{ "UserPaymentMethod"
"PaymentMethod" ||--o{ "UserPaymentMethod"
```
# Нормализация схемы базы данных
## Рассмотрим каждую таблицу и выявим функциональные зависимости между ее атрибутами:

Таблица "User":

user_id → bonus_account_id, name, email, phone, login

bonus_account_id → user_id, name, email, phone, login

email → user_id, name, bonus_account_id, phone, login

login → bonus_account_id, name, email, phone, user_id

Таблица "Partner":

partner_id → name, email, phone, login

login → name, email, phone, partner_id

email → name, login, phone, partner_id

Таблица "Bonus_Account":

bonus_account_id → user_id, transaction_id

user_id → bonus_account_id, transaction_id

transaction_id → user_id, bonus_account_id

Таблица "Bonus_Transaction":

transaction_id → bonus_account_id, transaction_date, amount, transaction_type

Таблица "Hotel":

hotel_id → partner_id, rating, hotel_name, address, city, contacts, description

Таблица "Review":

review_id → user_id, hotel_id, comment_text, date_creation

Таблица "Room":

room_id → hotel_id, capacity, price, description, room_type, contacts

Таблица "Additional_service":

service_id → price, service_name, service_description

Таблица "Booking":

booking_id → user_id, room_id, payment_id,
    check_in_date, check_out_date, guests_number, 
    status, price, date_creation, paid, 

payment_id → user_id, room_id, booking_id,
    check_in_date, check_out_date, guests_number, 
    status, price, date_creation, paid, 

Таблица "Payment":

payment_id → booking_id, payment_date, amount, payment_status, payment_method

Таблица "Booking_Additional_service":

(booking_id, service_id) → Ø

Таблица "PartnerType":

partner_type_id → type_name, description

Таблица "Amenity":

amenity_id → amenity_name, amenity_description

Таблица "HotelAmenity":

(hotel_id, amenity_id) → ∅

Таблица "RoomFacility":

facility_id → facility_name, facility_description

Таблица "RoomHasFacility":

(room_id, facility_id) → ∅

Таблица "PaymentMethod":

payment_method_id → method_name

Таблица "BookingStatusHistory":

booking_status_history_id → booking_id, old_status, new_status, changed_at

Таблица "UserPaymentMethod":

user_payment_method_id → user_id, payment_method_id, details

## Приведем в ПНФ.
Для этого нужно, что бы все его атрибуты являлись простыми. Поэтому раздели поле name, в котом сейчас хранится имя и фамилия пользователя, на 2 поля: name и second_name. Также разделим поле contacts на: phone и email.
## Приведем в ВНФ.
Для этого нужно, чтобы оно нахидилось в первой форме, а также каждый неключевой атрибут функционально полно зависит от первичного ключа.
### Приведем в ТНФ
ДЛя этого кужно, чтобы оно находилось во второй форме, и все неключевые атрибуты взаимно независимы и полностью зависят от первичного ключа.

## Итоговая схема базы данных

```plantuml
entity "User" {
  * user_id : serial
  name : varchar(255)
  second_name : varchar(255)
  email : varchar(255)
  phone : varchar(255)
  login : varchar(255)
  bonus_account_id : int <<FK>>
}

entity "Partner" {
  * partner_id : serial
  name : varchar(255)
  second_name : varchar(255)
  email : varchar(255)
  phone : varchar(255)
  login : varchar(255)
  partner_type_id : int <<FK>>
}

entity "Hotel" {
  * hotel_id : serial
  partner_id : int <<FK>>
  hotel_name : varchar(255)
  rating : int
  address : varchar(255)
  city : varchar(255)
  phone : varchar(255)
  email : varchar(255)
  description : varchar(255)
}

entity "Room" {
  * room_id : serial
  hotel_id : int <<FK>>
  description : varchar(255)
  room_type : varchar(255)
  capacity : int
  price : decimal
}

entity "Additional_service" {
  * service_id : serial
  service_name : varchar(255)
  service_description : varchar(255)
  price : decimal
}

entity "Booking" {
  * booking_id : serial
  user_id : int <<FK>>
  room_id : int <<FK>>
  payment_id : int <<FK>>
  check_in_date : date
  check_out_date : date
  guests_number : int
  status : enum
  price : decimal
  date_creation : date
  paid : enum
}

entity "Review" {
  * review_id : serial
  user_id : int <<FK>>
  hotel_id : int <<FK>>
  comment_text : text
  date_creation : date
}

entity "Bonus_Account" {
  * bonus_account_id : serial
  user_id : int <<FK>>
  transaction_id : int <<FK>>
}

entity "Booking_Additional_service" {
  booking_id : int <<FK>>
  service_id : int <<FK>>
}

entity "Payment" {
  * payment_id : serial
  booking_id : int <<FK>>
  payment_date : date
  amount : decimal
  payment_method_id : int <<FK>> ' Заменили строковое поле на FK
  payment_status : enum
}

entity "Bonus_Transaction" {
  * transaction_id : serial
  bonus_account_id : int <<FK>>
  transaction_date : date
  amount : decimal
  transaction_type : varchar(255)
}

entity "PartnerType" {
  * partner_type_id : serial
  type_name : varchar(255)
  description : varchar(255)
}

entity "Amenity" {
  * amenity_id : serial
  amenity_name : varchar(255)
  amenity_description : varchar(255)
}

entity "HotelAmenity" {
  hotel_id : int <<FK>>
  amenity_id : int <<FK>>
}

entity "RoomFacility" {
  * facility_id : serial
  facility_name : varchar(255)
  facility_description : varchar(255)
}

entity "RoomHasFacility" {
  room_id : int <<FK>>
  facility_id : int <<FK>>
}

entity "PaymentMethod" {
  * payment_method_id : serial
  method_name : varchar(255)
}

entity "BookingStatusHistory" {
  * booking_status_history_id : serial
  booking_id : int <<FK>>
  old_status : enum
  new_status : enum
  changed_at : date
}

entity "UserPaymentMethod" {
  * user_payment_method_id : serial
  user_id : int <<FK>>
  payment_method_id : int <<FK>>
  details : varchar(255)
}

"User" ||--o{ "Booking"
"Partner" ||--o{ "Hotel"
"Hotel" ||--o{ "Room"
"Room" ||--o{ "Booking"
"User" ||--o{ "Review"
"Hotel" ||--o{ "Review"
"User" ||--o| "Bonus_Account"
"Booking" ||--|| "Booking_Additional_service"
"Additional_service" ||--|| "Booking_Additional_service"
"Booking" ||--o{ "Payment"
"Bonus_Account" ||--o{ "Bonus_Transaction"

"PartnerType" ||--o{ "Partner"
"Amenity" ||--o{ "HotelAmenity"
"Hotel"   ||--o{ "HotelAmenity"
"RoomFacility" ||--o{ "RoomHasFacility"
"Room"         ||--o{ "RoomHasFacility"
"PaymentMethod" ||--o{ "Payment"
"Booking" ||--o{ "BookingStatusHistory"
"User"          ||--o{ "UserPaymentMethod"
"PaymentMethod" ||--o{ "UserPaymentMethod"
```