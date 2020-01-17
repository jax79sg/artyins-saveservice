
CREATE TABLE `reports` (
  #`id` int PRIMARY KEY AUTO_INCREMENT,
  `filename` varchar(255) PRIMARY KEY,
  `created_at` varchar(14),
  `ingested_at` varchar(14),
  `currentloc` varchar(255)
);

CREATE TABLE `ingests` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `text` text,
  `section` varchar(255),
  `created_at` varchar(14),
  `ingest_id` varchar(1000),
  `predicted_category` varchar(255),
  `annotated_category` varchar(255)
);

ALTER TABLE `ingests` ADD FOREIGN KEY (`ingest_id`) REFERENCES `reports` (`filename`);
GRANT ALL PRIVILEGES ON *.* TO 'user'@'%' identified by 'password';
INSERT INTO reports (filename,created_at,ingested_at,currentloc) VALUES ("hello.pdf","20191231121212","20191231121312","/home/user/reports/raw/");
INSERT INTO ingests (text, section, created_at, ingest_id, predicted_category, annotated_category) VALUES ('Hellow hellow','observation','20200121121313','hello.pdf','PERSONNEL','PERSONNEL');

commit;
