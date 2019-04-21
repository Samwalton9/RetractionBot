CREATE TABLE `retractions` (
  `type` varbinary(10) NOT NULL,
  `origin` varbinary(20) NOT NULL,
  `original_id` varbinary(50) NOT NULL,
  `retraction_id` varbinary(50) NOT NULL
) ENGINE=Aria;

CREATE TABLE `edit_log` (
  `timestamp` TIMESTAMP NOT NULL,
  `domain` varbinary(20) NOT NULL,
  `page_title` varbinary(255) NOT NULL,
  `original_id` varbinary(50) NOT NULL,
  `retraction_id` varbinary(50) NOT NULL
) ENGINE=Aria;