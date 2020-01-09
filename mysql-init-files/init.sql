
CREATE TABLE `reports` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `filename` varchar(255),
  `created_at` varchar(14),
  `ingested_at` varchar(14),
  `currentloc` varchar(255)
);

CREATE TABLE `ingests` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `text` varchar(255),
  `section` varchar(255),
  `created_at` varchar(14),
  `ingest_id` int,
  `predicted_category` varchar(255),
  `annotated_category` varchar(255)
);

ALTER TABLE `ingests` ADD FOREIGN KEY (`ingest_id`) REFERENCES `reports` (`id`);

INSERT INTO reports (filename,created_at,ingested_at,currentloc) VALUES ("hello.pdf","2019-12-31 12:12:12","2019-12-31 12:13:12","/home/user/reports/raw/");
INSERT INTO ingests (text, section, created_at, ingest_id, predicted_category, annotated_category) VALUES ('Hellow hellow','observation','2020-01-21 12:13:13',1,'PERSONNEL','PERSONNEL');

