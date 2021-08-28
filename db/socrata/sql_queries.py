CREATE_DB="""
CREATE DATABASE IF NOT EXISTS properly_db;
"""


DROP_TABLE_QUERY="""
DROP TABLE IF EXISTS socrata_data
"""

CREATE_TABLE_QUERY="""
CREATE TABLE IF NOT EXISTS socrata_data(
   id bigint,
   permit_ varchar(50),
   permit_type varchar(50),
   review_type varchar(50),
   application_start_date DATETIME,
   issue_date DATETIME,
   processing_time varchar(50),
   street_number varchar(20),
   street_direction varchar(2),
   street_name varchar(200),
   suffix varchar(50),
   work_description TEXT,
   building_fee_paid varchar(50),
   other_fee_paid varchar(10),
   subtotal_paid varchar(10),
   building_fee_unpaid varchar(10),
   zoning_fee_unpaid varchar(10),
   zoning_fee_paid varchar(10),
   other_fee_unpaid varchar(10),
   subtotal_unpaid varchar(10),
   building_fee_waived varchar(10),
   zoning_fee_waived varchar(10),
   other_fee_waived varchar(10),
   subtotal_waived varchar(10),
   total_fee varchar(200),
   reported_cost varchar(10),
   latitude float,
   longitude float
);

"""

INSERT_ROW = """
INSERT INTO socrata_data (
   id,
   permit_,
   permit_type,
   review_type,
   application_start_date,
   issue_date,
   processing_time,
   street_number,
   street_direction,
   street_name,
   suffix,
   work_description,
   building_fee_paid,
   zoning_fee_paid,
   other_fee_paid,
   subtotal_paid,
   building_fee_unpaid,
   zoning_fee_unpaid,
   other_fee_unpaid,
   subtotal_unpaid,
   building_fee_waived,
   zoning_fee_waived,
   other_fee_waived,
   subtotal_waived,
   total_fee,
   reported_cost,
   latitude,
   longitude
   
) VALUES(
%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
)
"""
