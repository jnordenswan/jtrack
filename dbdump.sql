PRAGMA foreign_keys=ON;
PRAGMA encoding = "UTF-8";
BEGIN TRANSACTION;

CREATE TABLE event (
id integer constraint pk primary key asc autoincrement constraint nn not null constraint uq unique,
name text constraint nn not null,
date integer constraint df default null,
duration integer constraint df default null,
recurrence text constraint df default null,
deadline integer constraint df default null);
INSERT INTO "event" VALUES(1,'lightsout',1380488400,21600,'86400,86400,86400,86400,259200',NULL);
INSERT INTO "event" VALUES(2,'morning routine',1380513600,7200,'86400,86400,86400,86400,259200',NULL);
INSERT INTO "event" VALUES(3,'clear kitchen',NULL,600,NULL,NULL);
INSERT INTO "event" VALUES(4,'eat breakfast',NULL,1200,NULL,NULL);
INSERT INTO "event" VALUES(5,'wash',NULL,1200,NULL,NULL);
INSERT INTO "event" VALUES(6,'set breakfast',NULL,600,NULL,NULL);
INSERT INTO "event" VALUES(7,'exercise',NULL,1800,NULL,NULL);
INSERT INTO "event" VALUES(8,'start breakfast',NULL,300,NULL,NULL);
INSERT INTO "event" VALUES(9,'quicken',NULL,900,NULL,NULL);

CREATE TABLE event_map (
parent INTEGER CONSTRAINT nn NOT NULL CONSTRAINT uq UNIQUE REFERENCES event(id) ON DELETE CASCADE,
child INTEGER CONSTRAINT nn NOT NULL CONSTRAINT uq UNIQUE REFERENCES event(id) ON DELETE CASCADE);
INSERT INTO "event_map" VALUES(2,3);
INSERT INTO "event_map" VALUES(3,4);
INSERT INTO "event_map" VALUES(4,5);
INSERT INTO "event_map" VALUES(5,6);
INSERT INTO "event_map" VALUES(6,7);
INSERT INTO "event_map" VALUES(7,8);
INSERT INTO "event_map" VALUES(8,9);

CREATE TABLE commitment (
id INTEGER CONSTRAINT pk PRIMARY KEY ASC AUTOINCREMENT CONSTRAINT nn NOT NULL CONSTRAINT uq UNIQUE,
draft_date INTEGER CONSTRAINT nn NOT NULL,
commit_date INTEGER CONSTRAINT df DEFAULT NULL,
review_date INTEGER CONSTRAINT df DEFAULT NULL);

CREATE TABLE commitment_map (
commitment_id INTEGER CONSTRAINT nn NOT NULL REFERENCES commitment(id) ON DELETE CASCADE,
event_id INTEGER CONSTRAINT nn NOT NULL CONSTRAINT uq UNIQUE REFERENCES event(id) ON DELETE RESTRICT,
resolved BOOLEAN CONSTRAINT nn NOT NULL CONSTRAINT df DEFAULT false);

DELETE FROM sqlite_sequence;
INSERT INTO "sqlite_sequence" VALUES('events',9);

COMMIT;

