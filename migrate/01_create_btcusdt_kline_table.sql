CREATE TABLE btcusdt_kline (
    open_time BIGINT,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume NUMERIC,
    close_time BIGINT,
    quote_volume NUMERIC,
    count INT,
    taker_buy_volume NUMERIC,
    taker_buy_quote_volume NUMERIC,
    ignore INT
);

CREATE INDEX idx_open_time ON btcusdt_kline (open_time);
