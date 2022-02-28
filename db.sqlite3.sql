BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id" serial NOT NULL,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL,
	PRIMARY KEY("id" )
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id" serial NOT NULL,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" )
);
CREATE TABLE IF NOT EXISTS "auth_user_groups" (
	"id" serial NOT NULL,
	"user_id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	PRIMARY KEY("id" ),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" (
	"id" serial NOT NULL,
	"user_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" ),
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_admin_log" (
	"id" serial NOT NULL,
	"action_time"	datetime NOT NULL,
	"object_id"	text,
	"object_repr"	varchar(200) NOT NULL,
	"change_message"	text NOT NULL,
	"content_type_id"	integer,
	"user_id"	integer NOT NULL,
	"action_flag"	smallint  NOT NULL CHECK("action_flag" >= 0),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" )
);
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id" serial NOT NULL,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL,
	PRIMARY KEY("id" )
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id" serial NOT NULL,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	PRIMARY KEY("id" ),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id" serial NOT NULL,
	"name"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" )
);
CREATE TABLE IF NOT EXISTS "auth_user" (
	"id" serial NOT NULL,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"username"	varchar(150) NOT NULL UNIQUE,
	"last_name"	varchar(150) NOT NULL,
	"email"	varchar(254) NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"first_name"	varchar(150) NOT NULL,
	PRIMARY KEY("id" )
);
CREATE TABLE IF NOT EXISTS "django_session" (
	"session_key"	varchar(40) NOT NULL,
	"session_data"	text NOT NULL,
	"expire_date"	datetime NOT NULL,
	PRIMARY KEY("session_key")
);
CREATE TABLE IF NOT EXISTS "polls_question" (
	"id" serial NOT NULL,
	"question_text"	varchar(200) NOT NULL,
	"pub_date"	datetime NOT NULL,
	PRIMARY KEY("id" )
);
CREATE TABLE IF NOT EXISTS "polls_choice" (
	"id" serial NOT NULL,
	"choice_text"	varchar(200) NOT NULL,
	"votes"	integer NOT NULL,
	"question_id"	bigint NOT NULL,
	PRIMARY KEY("id" ),
	FOREIGN KEY("question_id") REFERENCES "polls_question"("id") DEFERRABLE INITIALLY DEFERRED
);
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (1,'contenttypes','0001_initial','2022-02-10 18:34:25.509175'),
 (2,'auth','0001_initial','2022-02-10 18:34:25.526272'),
 (3,'admin','0001_initial','2022-02-10 18:34:25.540636'),
 (4,'admin','0002_logentry_remove_auto_add','2022-02-10 18:34:25.565388'),
 (5,'admin','0003_logentry_add_action_flag_choices','2022-02-10 18:34:25.575756'),
 (6,'contenttypes','0002_remove_content_type_name','2022-02-10 18:34:25.590571'),
 (7,'auth','0002_alter_permission_name_max_length','2022-02-10 18:34:25.600971'),
 (8,'auth','0003_alter_user_email_max_length','2022-02-10 18:34:25.611217'),
 (9,'auth','0004_alter_user_username_opts','2022-02-10 18:34:25.619917'),
 (10,'auth','0005_alter_user_last_login_null','2022-02-10 18:34:25.630525'),
 (11,'auth','0006_require_contenttypes_0002','2022-02-10 18:34:25.633389'),
 (12,'auth','0007_alter_validators_add_error_messages','2022-02-10 18:34:25.640500'),
 (13,'auth','0008_alter_user_username_max_length','2022-02-10 18:34:25.649144'),
 (14,'auth','0009_alter_user_last_name_max_length','2022-02-10 18:34:25.660762'),
 (15,'auth','0010_alter_group_name_max_length','2022-02-10 18:34:25.669968'),
 (16,'auth','0011_update_proxy_permissions','2022-02-10 18:34:25.676571'),
 (17,'auth','0012_alter_user_first_name_max_length','2022-02-10 18:34:25.686955'),
 (18,'sessions','0001_initial','2022-02-10 18:34:25.693987'),
 (19,'polls','0001_initial','2022-02-10 21:34:56.590330');
INSERT INTO "auth_user_user_permissions" ("id","user_id","permission_id") VALUES (1,2,25),
 (2,2,29);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","change_message","content_type_id","user_id","action_flag") VALUES (1,'2022-02-10 23:07:27.153418','2','giulio','[{"added": {}}]',4,1,1),
 (2,'2022-02-10 23:10:26.875525','2','giulio','[{"changed": {"fields": ["User permissions"]}}]',4,1,2),
 (3,'2022-02-13 11:32:15.704953','2','Ti piace il calcio  ?','[{"added": {}}]',8,1,1),
 (4,'2022-02-13 20:05:37.574258','1','Not much','[{"changed": {"fields": ["Votes"]}}]',7,1,2),
 (5,'2022-02-13 21:12:18.001488','2','The sky','[{"changed": {"fields": ["Question"]}}]',7,1,2),
 (6,'2022-02-13 21:12:43.183161','2','The sky','[{"changed": {"fields": ["Question"]}}]',7,1,2);
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (1,'admin','logentry'),
 (2,'auth','permission'),
 (3,'auth','group'),
 (4,'auth','user'),
 (5,'contenttypes','contenttype'),
 (6,'sessions','session'),
 (7,'polls','choice'),
 (8,'polls','question');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (1,1,'add_logentry','Can add log entry'),
 (2,1,'change_logentry','Can change log entry'),
 (3,1,'delete_logentry','Can delete log entry'),
 (4,1,'view_logentry','Can view log entry'),
 (5,2,'add_permission','Can add permission'),
 (6,2,'change_permission','Can change permission'),
 (7,2,'delete_permission','Can delete permission'),
 (8,2,'view_permission','Can view permission'),
 (9,3,'add_group','Can add group'),
 (10,3,'change_group','Can change group'),
 (11,3,'delete_group','Can delete group'),
 (12,3,'view_group','Can view group'),
 (13,4,'add_user','Can add user'),
 (14,4,'change_user','Can change user'),
 (15,4,'delete_user','Can delete user'),
 (16,4,'view_user','Can view user'),
 (17,5,'add_contenttype','Can add content type'),
 (18,5,'change_contenttype','Can change content type'),
 (19,5,'delete_contenttype','Can delete content type'),
 (20,5,'view_contenttype','Can view content type'),
 (21,6,'add_session','Can add session'),
 (22,6,'change_session','Can change session'),
 (23,6,'delete_session','Can delete session'),
 (24,6,'view_session','Can view session'),
 (25,7,'add_choice','Can add choice'),
 (26,7,'change_choice','Can change choice'),
 (27,7,'delete_choice','Can delete choice'),
 (28,7,'view_choice','Can view choice'),
 (29,8,'add_question','Can add question'),
 (30,8,'change_question','Can change question'),
 (31,8,'delete_question','Can delete question'),
 (32,8,'view_question','Can view question');
INSERT INTO "auth_user" ("id","password","last_login","is_superuser","username","last_name","email","is_staff","is_active","date_joined","first_name") VALUES (1,'pbkdf2_sha256$320000$4sKB3UVj3PJprFY5KwtVg4$M7/xOFvnt6WeqbDif8KKUyDN+vKlZJK0eSu/kkem2Sc=','2022-02-14 21:44:52.042483',1,'admin','','gfalco58@gmail.com',1,1,'2022-02-10 23:02:42.429688',''),
 (2,'pbkdf2_sha256$320000$CRlytNPyDonVhLa6D4ThEz$UULTy1AfKbps8Bh7mXUAAfk8H5/Cs59/Z4/UbhNR3Po=',NULL,0,'giulio','','',0,1,'2022-02-10 23:07:27','');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('znj7x5ba2f9jtff9o858k2kgg1o1ot20','.eJxVjDsOgzAQBe_iOrKM8W9TpucMaNe7xCQRSBiqKHcPSBRJ-2bmvVWP21r6rcrSj6yuqlGX340wP2U6AD9wus86z9O6jKQPRZ-06m5med1O9--gYC173ZqMjlqJwftATNnY0LTiPFiXokAKCcAMDmyTyUZgYcPOMw27jw7V5wvMKDeB:1nJCv2:oPnhw8l7SYDkRUcMjZYFOmMMtnmKhk-nO5Bo7fUo2a8','2022-02-27 11:19:52.020189');
INSERT INTO "polls_question" ("id","question_text","pub_date") VALUES (1,'What''s up ?','2022-02-11 18:02:08.071544'),
 (2,'Ti piace il calcio  ?','2022-02-13 11:31:42');
INSERT INTO "polls_choice" ("id","choice_text","votes","question_id") VALUES (1,'Not much',4,1),
 (2,'The sky',3,1),
 (3,'Just hacking again',0,1);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" (
	"user_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_group_id_97559544" ON "auth_user_groups" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" (
	"user_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" (
	"expire_date"
);
CREATE INDEX IF NOT EXISTS "polls_choice_question_id_c5b4b260" ON "polls_choice" (
	"question_id"
);
COMMIT;
