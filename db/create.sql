SET SEARCH_PATH TO read;

CREATE TYPE state AS ENUM(
    'pending',
    'complete',
    'reading'
);

CREATE TABLE book (
    id SERIAL PRIMARY KEY,
	username VARCHAR(50) NOT NULL,
	title VARCHAR(300) NOT NULL,
    des TEXT,
	status state NOT NULL DEFAULT 'pending',
	pct_read SMALLINT NOT NULL DEFAULT 0,
    start_read_date DATE,
    end_read_date DATE,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    --CHECK(status IN ('pending','compleat','reading'))
    
    --CONDITIONS
    /*
    IF STATUS='complete', then we want 'pct_read'=100
    else pct_read between 0 and 99 and status <> 'complete'
    */

    CHECK(
        pct_read=100 AND status='complete'
        OR
        pct_read BETWEEN 0 AND 99 AND status <> 'complete'
    )

);