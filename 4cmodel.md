## System Context diagram [Docs](https://c4model.com/)

## C1: Context Diagram

Shows the system in its environment and the interactions with external actors.

• External Exchange (e.g., Binance, Kraken): Provides real-time market data.
• Crypto Arbitrage System: The core system responsible for fetching data, detecting arbitrage, and executing trades.
• Trade Executor: Executes trades based on detected opportunities.

```
+-------------------+
| External Exchange |
|  (Binance, Kraken)|
+-------------------+
        |
        | Fetch market data
        v
+---------------------------------+
|   Crypto Arbitrage System       |
|---------------------------------|
| - Fetches market data           |
| - Translates data formats       |
| - Detects arbitrage opportunities|
| - Logs and executes trades      |
+---------------------------------+
        |
        | Detected arbitrage opportunities
        v
+-------------------+
|   Trade Executor  |
+-------------------+
```

## Container Diagram (C2)

Illustrates the high-level containers (applications, services, databases, etc.) that make up the
system.

• Market Data Fetcher: Fetches market data from external exchanges (Binance, Kraken, etc.).
• Message Broker (Kafka): A message broker that handles communication between different components.
• NEW_TRADING_PAIR Topic: A topic that carries translated market data.
• Message Translator: Translates exchange-specific data into a unified format.
• Arbitrage Detector: Detects arbitrage opportunities by comparing prices between exchanges.
• Trade Executor: Executes trades when arbitrage opportunities are detected.
• Logging System: Logs detected opportunities for audit and monitoring.

```
+-------------------------------+
|    Crypto Arbitrage System    |
|-------------------------------|
|                               |
|  +-------------------------+  |
|  | Market Data Fetcher     |  |     +---------------------------+
|  |-------------------------|  |---->|  Message Broker (Kafka)    |
|  | Fetches data from       |  |     | (NEW_TRADING_PAIR topic)   |
|  | external exchanges      |  |     +---------------------------+
|  +-------------------------+  |                  |
|                               |                  |
|  +-------------------------+  |                  |
|  | Message Translator      |  |<-----------------|
|  |-------------------------|  | Reads messages   |
|  | Translates exchange data|  | from topic       |
|  | to a unified format     |  |                  |
|  +-------------------------+  |                  |
|                               |                  |
|  +-------------------------+  |                  |
|  | Arbitrage Detector      |  |                  |
|  |-------------------------|  |                  |
|  | Detects arbitrage       |  |                  |
|  | opportunities by        |  |                  |
|  | comparing prices        |  |                  |
|  +-------------------------+  |                  |
|                               |                  |
|  +-------------------------+  |                  |
|  | Trade Executor          |  |                  |
|  |-------------------------|  |                  |
|  | Executes trades based on|  |                  |
|  | detected opportunities  |  |                  |
|  +-------------------------+  |                  |
|                               |                  |
|  +-------------------------+  |                  |
|  | Logging System          |  |                  |
|  |-------------------------|  |                  |
|  | Logs detected arbitrage |  |                  |
|  | opportunities           |  |                  |
|  +-------------------------+  |                  |
+-------------------------------+
```

## C3: Component Diagram for the Arbitrage Detector

The Component Diagram focuses on the internal components within the Arbitrage Detector container, detailing the
individual modules and how they interact.

#### Market Data Fetcher

```
+--------------------------------------+
|           Market Data Fetcher        |
|--------------------------------------|
|                                      |
| + ExchangeDataFetcher                |
|  |----------------------------------| 
|  | Fetches data from different      |
|  | exchanges using exchange-specific|
|  | fetchers                         |
| +-----------------------------------|
|                                      |
| + BinanceFetcher                     |
|  |----------------------------------| 
|  | Fetches data from Binance        |
|  | using ccxt API                   |
| +-----------------------------------|
|                                      |
| + KrakenFetcher                      |
|  |----------------------------------| 
|  | Fetches data from Kraken         |
|  | using ccxt API                   |
| +-----------------------------------|
|                                      |
| + NewExchangeFetcher                 |
|  |----------------------------------| 
|  | Fetches data from a new exchange |
|  | using exchange-specific methods  |
| +-----------------------------------|
+--------------------------------------+
```

#### Message Translator

```
+--------------------------------------+
|          Message Translator          |
|--------------------------------------|
|                                      |
| + TranslatorRegistry                 |
|  |----------------------------------| 
|  | Registers and manages translator |
|  | functions for each exchange      |
| +-----------------------------------|
|                                      |
| + BinanceTranslator                  |
|  |----------------------------------| 
|  | Translates data from Binance     |
|  | format to unified format         |
| +-----------------------------------|
|                                      |
| + KrakenTranslator                   |
|  |----------------------------------| 
|  | Translates data from Kraken      |
|  | format to unified format         |
| +-----------------------------------|
|                                      |
| + NewExchangeTranslator              |
|  |----------------------------------| 
|  | Translates data from new exchange|
|  | format to unified format         |
| +-----------------------------------|
+--------------------------------------+
```

#### Message Channel

```
+--------------------------------------+
|            Message Channel           |
|--------------------------------------|
|                                      |
| + KafkaProducer                      |
|  |----------------------------------| 
|  | Produces messages to Kafka       |
|  | topics (e.g., NEW_TRADING_PAIR)  |
| +-----------------------------------|
|                                      |
| + KafkaConsumer                      |
|  |----------------------------------| 
|  | Consumes messages from Kafka     |
|  | topics                           |
| +-----------------------------------|
+--------------------------------------+
```

#### Aggregator

```
+--------------------------------------+
|               Aggregator             |
|--------------------------------------|
|                                      |
| + AggregatorService                  |
|  |----------------------------------| 
|  | Collects and aggregates messages |
|  | from different exchanges by      |
|  | trading pair                     |
| +-----------------------------------|
|                                      |
| + MessageStorage                     |
|  |----------------------------------| 
|  | Stores the latest messages for   |
|  | each trading pair and exchange   |
| +-----------------------------------|
+--------------------------------------+
```

#### Arbitrage Detector

```
+--------------------------------------+
|               Aggregator             |
|--------------------------------------|
|                                      |
| + AggregatorService                  |
|  |----------------------------------| 
|  | Collects and stores market data  |
|  | from different exchanges by      |
|  | trading pair                     |
| +-----------------------------------|
|                                      |
| + MessageStorage                     |
|  |----------------------------------| 
|  | Stores the latest messages for   |
|  | each trading pair and exchange   |
| +-----------------------------------|
|                                      |
| + is_ready(symbol: str) -> bool      |  <-- Checks if data for a symbol is ready
|                                      |
| + get_aggregated_data(symbol: str)   |  <-- Retrieves aggregated data for comparison
|   -> dict                            |
+--------------------------------------+
```

#### Filter

```
+--------------------------------------+
|                 Filter               |
|--------------------------------------|
|                                      |
| + ArbitrageDetector                  |
|  |----------------------------------| 
|  | Detects arbitrage opportunities  |
|  | by comparing prices from         |
|  | different exchanges              |
| +-----------------------------------|
|                                      |
| + PriceComparator                    |
|  |----------------------------------| 
|  | Compares the prices for a trading|
|  | pair across exchanges            |
| +-----------------------------------|
|                                      |
| + OpportunityNotifier                |
|  |----------------------------------| 
|  | Sends detected arbitrage         |
|  | opportunities to the             |
|  | Publish-Subscribe Channel        |
| +-----------------------------------|
+--------------------------------------+
```

#### Publish-Subscribe Channel

```
+--------------------------------------+
|     Publish-Subscribe Channel        |
|--------------------------------------|
|                                      |
| + KafkaProducer                      |
|  |----------------------------------| 
|  | Produces messages to Kafka       |
|  | topics (e.g., ARBITRAGE_OPPORTUNITIES)|
| +-----------------------------------|
|                                      |
| + KafkaConsumer                      |
|  |----------------------------------| 
|  | Consumes messages from Kafka     |
|  | topics                           |
| +-----------------------------------|
|                                      |
| + LoggingSystem                      |
|  |----------------------------------| 
|  | Logs detected arbitrage          |
|  | opportunities                    |
| +-----------------------------------|
|                                      |
| + TradeExecutor                      |
|  |----------------------------------| 
|  | Executes trades based on         |
|  | detected opportunities           |
| +-----------------------------------|
+--------------------------------------+
```

#### Logging System

```
+--------------------------------------+
|            Logging System            |
|--------------------------------------|
|                                      |
| + Logger                             |
|  |----------------------------------| 
|  | Logs information about detected  |
|  | opportunities                    |
| +-----------------------------------|
|                                      |
| + LogStorage                         |
|  |----------------------------------| 
|  | Stores log files or sends them   |
|  | to a centralized logging server  |
| +-----------------------------------|
+--------------------------------------+
```

#### Trading Executor

```
+--------------------------------------+
|           Trading Executor           |
|--------------------------------------|
|                                      |
| + TradeExecutorService               |
|  |----------------------------------| 
|  | Executes trades using exchange   |
|  | APIs                             |
| +-----------------------------------|
|                                      |
| + TradeValidator                     |
|  |----------------------------------| 
|  | Validates if the trade is        |
|  | feasible or profitable           |
| +-----------------------------------|
+--------------------------------------+
```

## C4: Code-Level Diagram for the Aggregator Component (WIP)

The Code-Level Diagram provides a detailed view of the classes and methods within the Aggregator component.

• add_message: Adds a new message to the aggregator for a given symbol.
• is_ready: Checks if the aggregator has collected messages from all necessary exchanges for a given symbol.
• get_aggregated_data: Returns the aggregated data for a trading pair when all necessary messages are collected.
• reset: Resets the aggregator state for the next cycle of message collection.

```
+------------------------------------------+
|              Aggregator                  |
|------------------------------------------|
| + Aggregator(symbol: str, messages: dict)|
|                                          |
| + add_message(message: dict)             |  <-- Adds a message to the aggregator
| + is_ready() -> bool                     |  <-- Checks if enough data has been collected
| + get_aggregated_data() -> dict          |  <-- Returns aggregated data for comparison
| + reset()                                |  <-- Resets the aggregator for the next cycle
+------------------------------------------+
```