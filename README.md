# Tak AI Player

An intelligent Tak game player using **Minimax**, **Alpha-Beta Pruning**, and **BFS-based Heuristic Evaluation**.

## 📌 Project Overview

Tak is a two-player abstract strategy board game in which players compete to build a continuous road connecting two opposite edges of the board.

This project aims to develop an intelligent Tak-playing agent capable of analyzing board positions, generating legal moves, and selecting strategic actions using adversarial search algorithms.

The AI player will use the **Minimax algorithm** with **Alpha-Beta Pruning** to explore possible future game states and make decisions. A heuristic evaluation function based on **Breadth-First Search (BFS)** will estimate road connectivity and help the AI evaluate positions when a complete game search is not possible.

The initial implementation will focus on a **5×5 Tak board**.

## 🎯 Project Objectives

- Implement the core rules and mechanics of Tak.
- Represent the game board and piece stacks efficiently.
- Generate all legal moves, including placement and stack movement.
- Detect road connections and determine winning conditions.
- Implement Minimax for adversarial decision-making.
- Optimize the search process using Alpha-Beta Pruning.
- Develop a BFS-based heuristic to evaluate road connectivity.
- Test and compare the AI's performance under different search configurations.

## 🎮 Game Overview

Tak is played between two players, typically represented as White and Black.

### Board

- The initial implementation uses a 5×5 board.
- Each cell can contain an empty space or a stack of pieces.
- Pieces within a stack can belong to different players.

### Piece Types

| Piece | Description |
|---|---|
| Flat Stone | A regular piece that can contribute to building a road. |
| Standing Stone (Wall) | Blocks roads and cannot be covered by ordinary pieces. |
| Capstone | A special piece that can flatten a standing stone under specific movement conditions. |

### Main Game Mechanics

- Players take turns placing pieces or moving existing stacks.
- Stack movement allows a player to carry and distribute pieces across multiple cells.
- A road is formed by connecting the player's road pieces orthogonally.
- The objective is to connect two opposite board edges with a continuous road.

## 🧠 AI Algorithms

### 1. Minimax Algorithm

Minimax is used to select the best move by exploring possible future game states.

- The AI evaluates its possible moves.
- It considers the opponent's possible responses.
- It chooses the move that maximizes its outcome while assuming the opponent plays optimally.

### 2. Alpha-Beta Pruning

Alpha-Beta Pruning improves Minimax by eliminating branches that cannot affect the final decision.

This reduces the number of explored game states and allows the AI to search deeper within a reasonable time.

### 3. BFS-Based Heuristic Evaluation

Breadth-First Search (BFS) is used to analyze road connectivity on the board.

The heuristic evaluation will consider factors such as:

- The distance required to connect the player's road to the opposite edge.
- The opponent's road progress.
- Potential road connections.
- Strategic positioning of pieces.

The evaluation function will assign scores to board states to help the AI choose promising moves.

## 🛠️ Technologies & Tools

The project is planned to use the following technologies:

- **Python** – Main programming language.
- **Pygame** – Graphical user interface.
- **Git & GitHub** – Version control and collaboration.
- **pytest** – Unit testing and validation.

## 🧪 Experiments & Evaluation

The AI will be evaluated through experiments designed to measure its decision-making performance.

Planned experiments include:

### 1. Minimax vs. Minimax with Alpha-Beta Pruning

- Compare the number of explored nodes.
- Measure decision-making time.
- Evaluate the impact of pruning on search efficiency.

### 2. Search Depth Comparison

- Test different search depths.
- Analyze the relationship between search depth and decision time.
- Measure the number of explored game states.

### 3. Heuristic Evaluation

- Test how BFS-based road distance affects move selection.
- Analyze the AI's ability to build its own road and block the opponent.
- Evaluate the effectiveness of the heuristic in different board positions.

### 4. Gameplay Testing

- Test the AI against a human player.
- Evaluate its behavior in different board situations.
- Check the correctness of generated moves and game outcomes.

## 📚 Literature Review

The project will investigate academic research and technical resources related to:

- Adversarial Search in Two-Player Games.
- Minimax Algorithm.
- Alpha-Beta Pruning.
- Heuristic Evaluation Functions.
- Breadth-First Search (BFS).
- Pathfinding and Connectivity Analysis.

Relevant academic papers and references will be included in the final project documentation.

## 📊 Dataset

The project focuses on a search-based game-playing AI rather than a machine learning model that requires training data.

Game states and gameplay scenarios may be used for testing and evaluating the implemented algorithms. The dataset or test-case source will be documented as the project progresses.

## 🚀 Project Status

**Currently in Development**

The project is being developed incrementally, starting with the game engine and legal move generation, followed by AI implementation, interface development, and performance evaluation.

## 📄 License

No license has been selected for this project yet.
