

CREATE_TABLE_QUERY="""
CREATE TABLE IF NOT EXISTS kaggle_data(
   id bigint,
   date_ TIMESTAMP,
   price  decimal(12, 2),
   bedrooms int,
   bathrooms float,
   sqft_living int,
   sqft_lot int,
   view int,
   condition_ int,
   grade int,
   sqft_above int,
   yr_built int,
   yr_renovated int,
   zipcode varchar(10),
   lat float,
   long_ float,
   sqft_living15 int,
   sqft_lot15 int
);

"""

INSERT_ROW = """
INSERT INTO kaggle_data (
   id,
   date_,
   price,
   bedrooms,
   bathrooms,
   sqft_living,
   sqft_lot,
   view,
   condition_,
   grade,
   sqft_above,
   yr_built,
   yr_renovated,
   zipcode,
   lat,
   long_,
   sqft_living15,
   sqft_lot15
) VALUES(
%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
)
"""