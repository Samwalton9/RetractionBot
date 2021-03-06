CREATE TABLE `retractions` (
  `timestamp` TIMESTAMP NOT NULL,
  `type` varbinary(10) NOT NULL,
  `origin` varbinary(20) NOT NULL,
  `original_id` varbinary(200) NOT NULL,
  `retraction_id` varbinary(200) NOT NULL
) ENGINE=Aria;

CREATE TABLE `edit_log` (
  `timestamp` TIMESTAMP NOT NULL,
  `domain` varbinary(20) NOT NULL,
  `page_title` varbinary(255) NOT NULL,
  `original_id` varbinary(200) NOT NULL,
  `retraction_id` varbinary(200) NOT NULL
) ENGINE=Aria;