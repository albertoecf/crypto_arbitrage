# Crypto Arbitrage

Welcome to the **Crypto Arbitrage** project! This repository contains the codebase for an automated arbitrage trading
system that monitors cryptocurrency prices across multiple exchanges, detects arbitrage opportunities, and executes
trades to capitalize on price discrepancies.

## Overview

This project is designed to be modular and scalable, leveraging enterprise integration patterns such as messaging
channels, content-based routing, and more. The system is composed of several key components that communicate through
Kafka message queues, ensuring flexibility and resilience.

## Messaging System Architecture

![Messaging System Diagram](media/message_diagram.png)  
*Diagram of the messaging system architecture will be displayed here.*

## Development Phases with Messaging

### Phase 1: Setup and Market Data Collection

- Set up a Kafka server on the cloud.
- Implement a script to fetch real-time market data and publish it to the `market_data` queue. (We will use Cron Jobs to
  run it huorly)

### Phase 2: Arbitrage Detection

- Develop a consumer script that listens to the `market_data` queue, processes the data, and publishes potential trade
  opportunities to the `trade_orders` queue.

### Phase 3: Trade Execution

- Create a consumer script to listen to the `trade_orders` queue and execute trades based on the messages received.

### Phase 4: Logging and Reporting

- Implement a logging system to record trade results and generate performance reports.

### Phase 5: Testing and Refinement

- Test the system end-to-end with messaging in place and refine the logic to ensure seamless operation.

## Tools and Libraries

- **Message Broker:** Kafka
- **Python Libraries:**
    - `confluent_kafka` for Kafka integration
    - `ccxt` for exchange integration
    - `pandas` for data handling
    - `logging` for logging

## Final Deliverable

The final deliverable is a modular trading bot with components communicating via Kafka message queues, ensuring
flexibility, scalability, and resilience.

## Project Structure

- **Modular project structure** to organize core functionality, configurations, data, and scripts efficiently.
    - `src/arbitrage/`: Contains the core scripts for fetching market data, detecting arbitrage opportunities, executing
      trades, and logging/reporting.
    - `src/config/`: Houses configuration files for Kafka (`kafka_config.yaml`) and exchange
      APIs (`exchanges_config.yaml`).
    - `src/data/`: Directory to store logs and generated performance reports.
    - `src/scripts/`: Contains utility scripts, such as `run_hourly.sh` for scheduling tasks.