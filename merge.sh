#!/bin/bash
> setup.sql
cat setup_db.sql >> setup.sql
cat setup_countries.sql >> setup.sql
cat setup_denominations.sql >> setup.sql
cat setup_values.sql >> setup.sql
cat setup_coins.sql >> setup.sql
