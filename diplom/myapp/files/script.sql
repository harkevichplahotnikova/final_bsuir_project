CREATE OR REPLACE PROCEDURE SP_GET_SUBSCRIPTION_TYPES(type_id number, p_results OUT SYS_REFCURSOR)
AS
BEGIN
OPEN p_results FOR
SELECT type_id,
type_name,
type_desc,
type_price,
prediction_amount
FROM t_subscription_type
ORDER BY type_id;
END;
/




CREATE OR REPLACE PROCEDURE SP_GET_PLAYERS(player_id number, p_results OUT SYS_REFCURSOR)
AS
BEGIN
OPEN p_results FOR
SELECT     
    player_id,
    player_first_name,
    player_last_name,
    player_full_name,
    player_country,
    player_gender,
    player_height,
    player_weight
FROM t_player
ORDER BY  player_first_name ASC,
    player_last_name ASC;
END;
/




CREATE OR REPLACE PROCEDURE SP_GET_MATCHES(p_user_id number, p_results OUT SYS_REFCURSOR)
AS
BEGIN
OPEN p_results FOR
SELECT     
    match_id,
    t.match_name,
    match_desc,
    match_date,
    first_player_full_name,
    second_player_full_name,
    nvl(tp.PREDICTION_ID, 0) as IS_PREDICTED
FROM t_match t
LEFT JOIN t_prediction tp on tp.user_id = p_user_id and tp.match_name = t.match_name
WHERE match_date = (SELECT MAX(match_date) FROM t_match);
END;
/



CREATE OR REPLACE PROCEDURE SP_GET_PREDICTIONS(p_user_id number, p_results OUT SYS_REFCURSOR)
AS
BEGIN
OPEN p_results FOR
SELECT     
    prediction_id,
    user_id,
    user_prediction_id,
    match_name,
    prediction_status_code,
    prediction_result,
    prediction_date
FROM t_prediction
WHERE user_id = p_user_id
ORDER BY user_prediction_id DESC;
END;
/






CREATE OR REPLACE PROCEDURE SP_GET_USER_EMAIL(p_user_id number, p_results OUT SYS_REFCURSOR)
AS
BEGIN
OPEN p_results FOR
SELECT     
    id,
    email
FROM auth_user
WHERE id = p_user_id;
END;
/














CREATE OR REPLACE PROCEDURE SP_GET_SUBSCRIPTION_TYPES_BY_ID(p_type_id number, p_results OUT SYS_REFCURSOR)
AS
BEGIN
OPEN p_results FOR
SELECT type_id,
type_name,
type_desc,
type_price,
prediction_amount
FROM t_subscription_type
WHERE type_id = p_type_id;
END;
/






CREATE OR REPLACE PROCEDURE SP_LOAD_NEW_SUBSCRIPTION(p_user_id number, p_subscription_type_id number, p_days number)
AS
BEGIN
INSERT INTO t_subscription
(
    subscription_id,
    subscription_type_id,
    user_id,
    subscription_start_date,
    subscription_end_date
)
VALUES (
    (select nvl(max(subscription_id),0) from t_subscription) + 1,
    p_subscription_type_id,
    p_user_id,
    TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD'),
    TO_CHAR(CURRENT_TIMESTAMP + p_days, 'YYYYMMDD')
);
END;
/










CREATE OR REPLACE PROCEDURE SP_GET_MATCHES_BY_NAME(p_match_name varchar2, p_results OUT SYS_REFCURSOR)
AS
BEGIN
OPEN p_results FOR
SELECT     
    match_id,
    match_name,
    match_desc,
    match_date,
    first_player_full_name,
    second_player_full_name
FROM t_match
WHERE match_name = p_match_name;
END;
/






CREATE OR REPLACE PROCEDURE SP_LOAD_NEW_USER_PREDICTION(p_match_name varchar2, p_user_id number)
AS
BEGIN
INSERT INTO t_prediction
(
    prediction_id,
    user_id,
    user_prediction_id,
    match_name,
    prediction_status_code,
    prediction_result,
    prediction_date
)
VALUES (
   (select nvl(max(prediction_id),0) from t_prediction) + 1,
    p_user_id,
    (select nvl(max(user_prediction_id),0) from t_prediction where user_id = p_user_id) + 1,
    p_match_name,
    'in progress',
    'in progress',
    TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD')
);
END;
/










CREATE OR REPLACE PROCEDURE SP_GET_SUBSCRIPTION_ANALYSIS(p_subscription_id varchar2, p_results OUT SYS_REFCURSOR)
AS
BEGIN
OPEN p_results FOR
SELECT   
    c.number_date,
    COUNT(t.subscription_id) as total_subs,
    COUNT(CASE WHEN t.subscription_start_date = c.number_date then t.subscription_id else null end) as start_subs,
    COUNT(CASE WHEN t.subscription_end_date = c.number_date then t.subscription_id else null end) as end_subs
FROM t_subscription t
JOIN calendar c on c.number_date between t.subscription_start_date and t.subscription_end_date
GROUP BY c.number_date;
END;
/














CREATE OR REPLACE PROCEDURE SP_GET_CURRENT_USER_PREDICTIONS_AMOUNT(p_user_id number, p_results OUT SYS_REFCURSOR)
AS
BEGIN
OPEN p_results FOR
with cte_user_subscription as (
    select user_id, 
           max(subscription_id) as subscription_id
    from t_subscription
    where user_id  = p_user_id
    group by user_id
)
, cte_subscription_user_info as (
    select t.user_id, 
           t.subscription_id,
           t.subscription_type_id,
           t.subscription_start_date,
           t.subscription_end_date
    from t_subscription t
    join cte_user_subscription c on  c.subscription_id = t.subscription_id
    where to_number(to_char(current_timestamp, 'YYYYMMDD')) between t.subscription_start_date and t.subscription_end_date
)
SELECT nvl(MAX(tst.PREDICTION_AMOUNT), 0) - COUNT(t.PREDICTION_ID) as PREDICTION_COUNT
FROM cte_subscription_user_info c 
LEFT JOIN t_prediction t on c.USER_ID = t.USER_ID and t.PREDICTION_DATE = to_number(to_char(current_timestamp, 'YYYYMMDD'))
LEFT JOIN t_subscription_type tst on c.subscription_type_id = tst.type_id;
END;
/






















CREATE OR REPLACE PROCEDURE SP_GET_CURRENT_USER_SUBSCRIPTION(p_user_id number, p_results OUT SYS_REFCURSOR)
AS
BEGIN
OPEN p_results FOR
WITH cte_max_subscription as (
    select MAX(SUBSCRIPTION_ID) as SUBSCRIPTION_ID
    from t_subscription
    where user_id = p_user_id
)
SELECT nvl(t.SUBSCRIPTION_TYPE_ID, -1) as SUBSCRIPTION_TYPE_ID
FROM cte_max_subscription c
LEFT JOIN t_subscription t on c.SUBSCRIPTION_ID = t.SUBSCRIPTION_ID;
END;
/






CREATE OR REPLACE PROCEDURE SP_GET_MATCHES_BY_PLAYER_ID(p_player_id number, p_results OUT SYS_REFCURSOR)
AS
BEGIN
OPEN p_results FOR
SELECT     
    match_id,
    match_name,
    match_desc,
    match_date,
    first_player_full_name,
    second_player_full_name
FROM t_match
JOIN t_player on  first_player_full_name = player_full_name or second_player_full_name = player_full_name
WHERE player_id = p_player_id;
END;
/


drop table t_subscription_type;
create table t_subscription_type (
    type_id number,
    type_name varchar2(500),
    type_desc varchar2(2000),
    type_price decimal (5,2),
    prediction_amount number,
    constraint pk_type_id primary key (type_id)
);



insert into t_subscription_type
(
type_id,
type_name,
type_desc,
type_price,
prediction_amount
)
values ( 1, 'Trial', 'can be you first subscription, free for 7 days, 2 predictions per day', 0, 2); 




insert into t_subscription_type
(
type_id,
type_name,
type_desc,
type_price,
prediction_amount
)
values (2, 'Standart', 'valid for 30 days, 20 predictions per day', 4.99, 20);



insert into t_subscription_type
(
type_id,
type_name,
type_desc,
type_price,
prediction_amount
)
values (3, 'Gold','valid for 30 days, 50 predictions per day', 9.99, 50);


insert into t_subscription_type
(
type_id,
type_name,
type_desc,
type_price,
prediction_amount
)
values (4, 'Platinum','valid for 30 days, 100 predictions per day', 17.99, 100);


drop table t_player;
create table t_player (
    player_id number,
    player_first_name varchar2(500),
    player_last_name varchar2(500),
    player_full_name varchar2(500),
    player_country varchar2(500),
    player_gender  varchar2(500),
    player_height  number,
    player_weight  number,
    constraint pk_player_id primary key (player_id)
);


drop table t_match
create table t_match (
    match_id number,
    match_name varchar2(500),
    match_desc varchar2(500),
    match_date number,
    first_player_full_name varchar2(500),
    second_player_full_name varchar2(500),
    constraint pk_match_id primary key (match_id)
);




drop table t_prediction
create table t_prediction (
    prediction_id number,
    user_id number,
    user_prediction_id number,
    match_name varchar2(500),
    prediction_status_code varchar2(500),
    prediction_result varchar2(500),
    prediction_date number,
    constraint pk_prediction_id primary key (prediction_id)
);


create table t_subscription(
    subscription_id number,
    subscription_type_id number,
    user_id number,
    subscription_start_date number,
    subscription_end_date   number,
    constraint pk_subscription_id primary key (subscription_id)
);



