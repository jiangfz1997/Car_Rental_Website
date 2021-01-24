

CREATE TABLE fjyh_corporation (
    cor_id          VARCHAR2(10 CHAR) NOT NULL,
    cor_name        VARCHAR2(30 CHAR) NOT NULL,
    cor_reg_number  VARCHAR2(20 CHAR) NOT NULL
);

COMMENT ON COLUMN fjyh_corporation.cor_id IS
    'CORPORATION ID';

COMMENT ON COLUMN fjyh_corporation.cor_name IS
    'CORPORATION NAME';

COMMENT ON COLUMN fjyh_corporation.cor_reg_number IS
    'CORPORATION REGISTRATION NUMBER';

ALTER TABLE fjyh_corporation ADD CONSTRAINT fjyh_corporation_pk PRIMARY KEY ( cor_id );

CREATE TABLE fjyh_coupon (
    coupid      VARCHAR2(10 CHAR) NOT NULL,
    type        VARCHAR2(10 CHAR) NOT NULL,
    percentage  NUMBER(3, 2) NOT NULL,
    rid         VARCHAR2(20 CHAR),
    is_corp     NUMBER NOT NULL,
    cor_id      VARCHAR2(10 CHAR),
    valid_from  DATE,
    valid_to    DATE
);

COMMENT ON COLUMN fjyh_coupon.coupid IS
    'COUPON ID';

COMMENT ON COLUMN fjyh_coupon.type IS
    'TYPE OF DISCOUNT- INDIVIDUAL, COPORATION';

COMMENT ON COLUMN fjyh_coupon.percentage IS
    'PERCENTAGE OF DISCOUNT';

COMMENT ON COLUMN fjyh_coupon.is_corp IS
    'WHETHER THIS COUPON IS A CORPORATION COUPON OR NOT';

COMMENT ON COLUMN fjyh_coupon.valid_from IS
    'THE START DATE OF COUPON VALIDATION';

COMMENT ON COLUMN fjyh_coupon.valid_to IS
    'THE END DATE OF COUPON VALIDATION';

CREATE UNIQUE INDEX fjyh_coupon__idx ON
    fjyh_coupon (
        rid
    ASC );

ALTER TABLE fjyh_coupon ADD CONSTRAINT fjyh_coupon_pk PRIMARY KEY ( coupid );

CREATE TABLE fjyh_coupon_customer (
    coupid  VARCHAR2(10 CHAR) NOT NULL,
    cid     VARCHAR2(20) NOT NULL
);

ALTER TABLE fjyh_coupon_customer ADD CONSTRAINT fjyh_coupon_customer_pk PRIMARY KEY ( coupid,
                                                                                      cid );

CREATE TABLE fjyh_cus_corporate (
    cid     VARCHAR2(20) NOT NULL,
    emp_id  VARCHAR2(20) NOT NULL,
    cor_id  VARCHAR2(10 CHAR) NOT NULL
);

COMMENT ON COLUMN fjyh_cus_corporate.cid IS
    'CUSTOMER ID';

COMMENT ON COLUMN fjyh_cus_corporate.emp_id IS
    'EMPLOYEE ID';

ALTER TABLE fjyh_cus_corporate ADD CONSTRAINT fjyh_cus_corporate_pk PRIMARY KEY ( cid );

ALTER TABLE fjyh_cus_corporate ADD CONSTRAINT fjyh_cus_corporate_pkv1 UNIQUE ( cor_id );

CREATE TABLE fjyh_cus_individual (
    cid             VARCHAR2(20) NOT NULL,
    dlnumber        VARCHAR2(20) NOT NULL,
    insuranceco     VARCHAR2(30) NOT NULL,
    ins_policy_num  VARCHAR2(20) NOT NULL
);

COMMENT ON COLUMN fjyh_cus_individual.cid IS
    'CUSTOMER ID';

COMMENT ON COLUMN fjyh_cus_individual.dlnumber IS
    'DRIVER LICENSE NUMBER OF CUSTOMER';

COMMENT ON COLUMN fjyh_cus_individual.insuranceco IS
    'INSURANCE COMPANY';

ALTER TABLE fjyh_cus_individual ADD CONSTRAINT fjyh_cus_individual_pk PRIMARY KEY ( cid );

CREATE TABLE fjyh_customer (
    cid             VARCHAR2(20) NOT NULL,
    cus_type        VARCHAR2(1) NOT NULL,
    cus_country     VARCHAR2(10) NOT NULL,
    cus_state       VARCHAR2(10) NOT NULL,
    cus_city        VARCHAR2(20) NOT NULL,
    cus_street      VARCHAR2(30) NOT NULL,
    cus_zipcode     NUMBER(5) NOT NULL,
    cus_email       VARCHAR2(30) NOT NULL,
    cus_phone       VARCHAR2(20) NOT NULL,
    cus_first_name  VARCHAR2(20) NOT NULL,
    cus_last_name   VARCHAR2(20) NOT NULL
);

ALTER TABLE fjyh_customer
    ADD CONSTRAINT ch_inh_fjyh_customer CHECK ( cus_type IN ( 'C', 'I' ) );

COMMENT ON COLUMN fjyh_customer.cid IS
    'CUSTOMER ID';

COMMENT ON COLUMN fjyh_customer.cus_type IS
    'CUSTOMER TYPE, ''I'' FOR INDIVIDUAL, ''C'' FOR CORPORATION';

COMMENT ON COLUMN fjyh_customer.cus_country IS
    'COUNTRY OF CUSTOMER ADDRESS';

COMMENT ON COLUMN fjyh_customer.cus_state IS
    'STATE OF CUSTOMER ADDRESS';

COMMENT ON COLUMN fjyh_customer.cus_city IS
    'CITY OF CUSTOMER ADDRESS';

COMMENT ON COLUMN fjyh_customer.cus_street IS
    'STREET OF CUSTOMER ADDRESS';

COMMENT ON COLUMN fjyh_customer.cus_zipcode IS
    'ZIPCODE OF CUSTOMER';

COMMENT ON COLUMN fjyh_customer.cus_email IS
    'CUSTOMER EMAIL ADDRESS';

COMMENT ON COLUMN fjyh_customer.cus_phone IS
    'CUSTOMER PHONE NUMBER';

COMMENT ON COLUMN fjyh_customer.cus_first_name IS
    'CUSTOMER FIRST NAME';

COMMENT ON COLUMN fjyh_customer.cus_last_name IS
    'CUSTOMER LAST NAME';

ALTER TABLE fjyh_customer ADD CONSTRAINT fjyh_customer_pk PRIMARY KEY ( cid );

CREATE TABLE fjyh_invoice (
    ivid                 VARCHAR2(10 CHAR) NOT NULL,
    iv_date              DATE NOT NULL,
    iv_amount            NUMBER(10, 2) NOT NULL,
    rid                  VARCHAR2(20 CHAR) NOT NULL,
    iv_remaining_amount  NUMBER(10, 2) NOT NULL,
    iv_status            VARCHAR2(1) NOT NULL
);

COMMENT ON COLUMN fjyh_invoice.ivid IS
    'INVOICE ID';

COMMENT ON COLUMN fjyh_invoice.iv_date IS
    'INVOICE DATE';

COMMENT ON COLUMN fjyh_invoice.iv_amount IS
    'AMOUNT OF THE INVOICE';

COMMENT ON COLUMN fjyh_invoice.iv_remaining_amount IS
    'THE REMAINING AMOUNT OF THE INVOICE';

COMMENT ON COLUMN fjyh_invoice.iv_status IS
    'INVOICE STATUS';

CREATE UNIQUE INDEX fjyh_invoice__idx ON
    fjyh_invoice (
        rid
    ASC );

ALTER TABLE fjyh_invoice ADD CONSTRAINT fjyh_invoice_pk PRIMARY KEY ( ivid );

CREATE TABLE fjyh_office (
    oid          VARCHAR2(20 CHAR) NOT NULL,
    ofc_country  VARCHAR2(20 CHAR) NOT NULL,
    ofc_state    VARCHAR2(2 CHAR) NOT NULL,
    ofc_city     VARCHAR2(20 CHAR) NOT NULL,
    ofc_street   VARCHAR2(30 CHAR) NOT NULL,
    ofc_zipcode  NUMBER(5) NOT NULL,
    ofc_phone    VARCHAR2(20 CHAR) NOT NULL
);

COMMENT ON COLUMN fjyh_office.oid IS
    'OFFICE ID';

COMMENT ON COLUMN fjyh_office.ofc_country IS
    'COUNTRY OF THE OFFICE';

COMMENT ON COLUMN fjyh_office.ofc_state IS
    'STATE OF THE OFFICE';

COMMENT ON COLUMN fjyh_office.ofc_city IS
    'CITY OF THE OFFICE';

COMMENT ON COLUMN fjyh_office.ofc_street IS
    'STREET ADDRESS';

COMMENT ON COLUMN fjyh_office.ofc_zipcode IS
    'ZIPCODE OF OFFICE';

COMMENT ON COLUMN fjyh_office.ofc_phone IS
    'OFFICE PHONE NUMBER';

ALTER TABLE fjyh_office ADD CONSTRAINT fjyh_office_pk PRIMARY KEY ( oid );

CREATE TABLE fjyh_payment (
    pid         VARCHAR2(10 CHAR) NOT NULL,
    pay_date    DATE NOT NULL,
    pay_amount  NUMBER(10, 2) NOT NULL,
    ivid        VARCHAR2(10 CHAR) NOT NULL,
    card_num    VARCHAR2(20 CHAR) NOT NULL,
    card_type   VARCHAR2(10 CHAR) NOT NULL
);

COMMENT ON COLUMN fjyh_payment.pid IS
    'PAYMENT ID';

COMMENT ON COLUMN fjyh_payment.pay_date IS
    'DATE OF PAYMENT';

COMMENT ON COLUMN fjyh_payment.pay_amount IS
    'AMOUNT OF THE PAYMENT';

COMMENT ON COLUMN fjyh_payment.card_num IS
    'CARD NUMBER';

COMMENT ON COLUMN fjyh_payment.card_type IS
    'CARD TYPE CREDIT DEBIT GIFT';

ALTER TABLE fjyh_payment ADD CONSTRAINT fjyh_payment_pk PRIMARY KEY ( pid,
                                                                      ivid );

CREATE TABLE fjyh_rental_service (
    rid                VARCHAR2(20 CHAR) NOT NULL,
    pick_date          DATE NOT NULL,
    drop_date          DATE NOT NULL,
    start_odometer     NUMBER(6, 3) NOT NULL,
    end_odometer       NUMBER(6, 3) NOT NULL,
    daily_limit        NUMBER(6, 3),
    ivid               VARCHAR2(10 CHAR) NOT NULL,
    vid                NUMBER(5),
    status             VARCHAR2(1) NOT NULL,
    coupid             VARCHAR2(10 CHAR),
    pickup_office_id   VARCHAR2(20 CHAR) NOT NULL,
    type_id            NUMBER,
    cid                VARCHAR2(20) NOT NULL,
    dropoff_office_id  VARCHAR2(20 CHAR) NOT NULL
);

COMMENT ON COLUMN fjyh_rental_service.rid IS
    'ID OF THE RENTAL SERVICE';

COMMENT ON COLUMN fjyh_rental_service.pick_date IS
    'PICK UP DATE';

COMMENT ON COLUMN fjyh_rental_service.drop_date IS
    'DROPOFF DATE';

COMMENT ON COLUMN fjyh_rental_service.start_odometer IS
    'START ODOMETER';

COMMENT ON COLUMN fjyh_rental_service.end_odometer IS
    'END ODOMETER';

COMMENT ON COLUMN fjyh_rental_service.daily_limit IS
    'DAILY ODOMETER LIMIT FOR THE RENTAL SERVICE';

COMMENT ON COLUMN fjyh_rental_service.status IS
    'STATUS OF RENTAL SERVICE P U F';

COMMENT ON COLUMN fjyh_rental_service.pickup_office_id IS
    'PICKUP OFFICE ID';

COMMENT ON COLUMN fjyh_rental_service.dropoff_office_id IS
    'DROPOFF OFFICE ID';

CREATE UNIQUE INDEX fjyh_rental_service__idx ON
    fjyh_rental_service (
        coupid
    ASC );

CREATE UNIQUE INDEX fjyh_rental_service__idxv1 ON
    fjyh_rental_service (
        ivid
    ASC );

ALTER TABLE fjyh_rental_service ADD CONSTRAINT fjyh_rental_service_pk PRIMARY KEY ( rid );

CREATE TABLE fjyh_vehicle (
    vid            NUMBER(5) NOT NULL,
    vin            VARCHAR2(20 CHAR) NOT NULL,
    make           VARCHAR2(20 CHAR) NOT NULL,
    model          VARCHAR2(10 CHAR) NOT NULL,
    year           DATE NOT NULL,
    lpn            VARCHAR2(15 CHAR) NOT NULL,
    oid            VARCHAR2(20 CHAR) NOT NULL,
    vehicle_class  VARCHAR2(20) NOT NULL,
    type_id        NUMBER NOT NULL
);

COMMENT ON COLUMN fjyh_vehicle.vin IS
    'VEHICLE IDENTIFICATION NUMBER';

COMMENT ON COLUMN fjyh_vehicle.make IS
    'MAKE OF THE VEHICLE';

COMMENT ON COLUMN fjyh_vehicle.model IS
    'MODEL TYPE OF THE VEHICLE';

COMMENT ON COLUMN fjyh_vehicle.year IS
    'YEAR OF THE VEHICLE';

COMMENT ON COLUMN fjyh_vehicle.lpn IS
    'LICENSE PLATE NUMBER';

ALTER TABLE fjyh_vehicle ADD CONSTRAINT fjyh_vehicle_pk PRIMARY KEY ( vid,
                                                                      type_id );

CREATE TABLE fjyh_vehicle_class (
    type_id       NUMBER NOT NULL,
    type          VARCHAR2(20) NOT NULL,
    rent_charge   NUMBER(10, 2) NOT NULL,
    extra_charge  NUMBER(10, 2) NOT NULL
);

COMMENT ON COLUMN fjyh_vehicle_class.type_id IS
    'TYPE ID OF VEHICLE CLASS';

COMMENT ON COLUMN fjyh_vehicle_class.type IS
    'TYPE OF VEHICLE CLASS';

COMMENT ON COLUMN fjyh_vehicle_class.rent_charge IS
    'RENT CHARGE OF VEHICLE CLASS';

COMMENT ON COLUMN fjyh_vehicle_class.extra_charge IS
    'EXTRA CHARGE OF VEHICLE CLASS';

ALTER TABLE fjyh_vehicle_class ADD CONSTRAINT fjyh_vehicle_class_pk PRIMARY KEY ( type_id );

ALTER TABLE fjyh_coupon
    ADD CONSTRAINT fjyh_corporation_fk FOREIGN KEY ( cor_id )
        REFERENCES fjyh_corporation ( cor_id );

ALTER TABLE fjyh_cus_corporate
    ADD CONSTRAINT fjyh_corporation_fkv1 FOREIGN KEY ( cor_id )
        REFERENCES fjyh_corporation ( cor_id );

--  ERROR: FK name length exceeds maximum allowed length(30) 
ALTER TABLE fjyh_coupon_customer
    ADD CONSTRAINT fjyh_coupon_customer_fjyh_coupon_fk FOREIGN KEY ( coupid )
        REFERENCES fjyh_coupon ( coupid );

--  ERROR: FK name length exceeds maximum allowed length(30) 
ALTER TABLE fjyh_coupon_customer
    ADD CONSTRAINT fjyh_coupon_customer_fjyh_customer_fk FOREIGN KEY ( cid )
        REFERENCES fjyh_customer ( cid );

ALTER TABLE fjyh_rental_service
    ADD CONSTRAINT fjyh_coupon_fk FOREIGN KEY ( coupid )
        REFERENCES fjyh_coupon ( coupid );

ALTER TABLE fjyh_rental_service
    ADD CONSTRAINT fjyh_customer_fk FOREIGN KEY ( cid )
        REFERENCES fjyh_customer ( cid );

ALTER TABLE fjyh_cus_corporate
    ADD CONSTRAINT fjyh_customer_fkv1 FOREIGN KEY ( cid )
        REFERENCES fjyh_customer ( cid );

ALTER TABLE fjyh_cus_individual
    ADD CONSTRAINT fjyh_customer_fkv2 FOREIGN KEY ( cid )
        REFERENCES fjyh_customer ( cid );

ALTER TABLE fjyh_rental_service
    ADD CONSTRAINT fjyh_invoice_fk FOREIGN KEY ( ivid )
        REFERENCES fjyh_invoice ( ivid );

ALTER TABLE fjyh_payment
    ADD CONSTRAINT fjyh_invoice_fkv1 FOREIGN KEY ( ivid )
        REFERENCES fjyh_invoice ( ivid );

ALTER TABLE fjyh_vehicle
    ADD CONSTRAINT fjyh_office_fk FOREIGN KEY ( oid )
        REFERENCES fjyh_office ( oid );

ALTER TABLE fjyh_rental_service
    ADD CONSTRAINT fjyh_office_fkv1 FOREIGN KEY ( pickup_office_id )
        REFERENCES fjyh_office ( oid );

ALTER TABLE fjyh_rental_service
    ADD CONSTRAINT fjyh_office_fkv2 FOREIGN KEY ( dropoff_office_id )
        REFERENCES fjyh_office ( oid );

ALTER TABLE fjyh_invoice
    ADD CONSTRAINT fjyh_rental_service_fk FOREIGN KEY ( rid )
        REFERENCES fjyh_rental_service ( rid );

ALTER TABLE fjyh_coupon
    ADD CONSTRAINT fjyh_rental_service_fkv1 FOREIGN KEY ( rid )
        REFERENCES fjyh_rental_service ( rid );

ALTER TABLE fjyh_vehicle
    ADD CONSTRAINT fjyh_vehicle_class_fk FOREIGN KEY ( type_id )
        REFERENCES fjyh_vehicle_class ( type_id );

ALTER TABLE fjyh_rental_service
    ADD CONSTRAINT fjyh_vehicle_fk FOREIGN KEY ( vid,
                                                 type_id )
        REFERENCES fjyh_vehicle ( vid,
                                  type_id );

CREATE OR REPLACE TRIGGER arc_fkarc__fjyh_cus_individual BEFORE
    INSERT OR UPDATE OF cid ON fjyh_cus_individual
    FOR EACH ROW
DECLARE
    d VARCHAR2(1);
BEGIN
    SELECT
        a.cus_type
    INTO d
    FROM
        fjyh_customer a
    WHERE
        a.cid = :new.cid;

    IF ( d IS NULL OR d <> 'I' ) THEN
        raise_application_error(-20223,
                               'FK FJYH_CUSTOMER_FKv2 in Table FJYH_CUS_INDIVIDUAL violates Arc constraint on Table FJYH_CUSTOMER - discriminator column CUS_TYPE doesn''t have value ''I''');
    END IF;

EXCEPTION
    WHEN no_data_found THEN
        NULL;
    WHEN OTHERS THEN
        RAISE;
END;
/

CREATE OR REPLACE TRIGGER arc_fkarc_1_fjyh_cus_corporate BEFORE
    INSERT OR UPDATE OF cid ON fjyh_cus_corporate
    FOR EACH ROW
DECLARE
    d VARCHAR2(1);
BEGIN
    SELECT
        a.cus_type
    INTO d
    FROM
        fjyh_customer a
    WHERE
        a.cid = :new.cid;

    IF ( d IS NULL OR d <> 'C' ) THEN
        raise_application_error(-20223,
                               'FK FJYH_CUSTOMER_FKv1 in Table FJYH_CUS_CORPORATE violates Arc constraint on Table FJYH_CUSTOMER - discriminator column CUS_TYPE doesn''t have value ''C''');
    END IF;

EXCEPTION
    WHEN no_data_found THEN
        NULL;
    WHEN OTHERS THEN
        RAISE;
END;
/



