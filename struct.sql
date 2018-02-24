create table users(
	id INTEGER primary key autoincrement,
	name text,
	email text,
	username char(255)
);

-- Source seeds
INSERT INTO source (id,img,name,object_id,created_date,updated_date) select(select lower(hex(randomblob(16))) AS UUID ),"http://placeholdit.com/200/200","android weekly",(select lower(hex(randomblob(16)))) AS UUID,(select current_timestamp as current_time),(select current_timestamp as current_time);
INSERT INTO source (id,img,name,object_id,created_date,updated_date) select(select lower(hex(randomblob(16))) AS UUID ),"http://placeholdit.com/200/200","android weekly",(select lower(hex(randomblob(16)))) AS UUID,(select current_timestamp as current_time),(select current_timestamp as current_time);
INSERT INTO source (id,img,name,object_id,created_date,updated_date) select(select lower(hex(randomblob(16))) AS UUID ),"http://placeholdit.com/200/200","android weekly",(select lower(hex(randomblob(16)))) AS UUID,(select current_timestamp as current_time),(select current_timestamp as current_time);