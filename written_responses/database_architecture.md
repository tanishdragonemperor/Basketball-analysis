# Database Architecture

## Overview
The basketball statistics database is designed as a normalized PostgreSQL schema with five main entities: Teams, Games, Players, Shots, Passes, and Turnovers. This design ensures data integrity, eliminates redundancy, and provides efficient querying capabilities for basketball analytics.

## Entity Relationship Design

### Core Entities

**Teams Table**
- Primary Key: `team_id` (Integer)
- Attributes: `name` (VARCHAR)
- Purpose: Stores team information and serves as reference for players

**Games Table** 
- Primary Key: `game_id` (Integer)
- Attributes: `date` (DATE)
- Purpose: Tracks game dates and provides temporal context for all events

**Players Table**
- Primary Key: `player_id` (Integer)
- Attributes: `name` (VARCHAR), `team_id` (Foreign Key → Teams)
- Purpose: Links players to their teams and serves as the central entity for all player actions

### Event Entities

**Shots Table**
- Primary Key: `shot_id` (Integer)
- Foreign Keys: `player_id` → Players, `game_id` → Games
- Attributes: `points`, `shooting_foul_drawn`, `shot_loc_x`, `shot_loc_y`, `action_type`
- Purpose: Records all shot attempts with spatial and contextual data

**Passes Table**
- Primary Key: `pass_id` (Integer) 
- Foreign Keys: `player_id` → Players, `game_id` → Games
- Attributes: `completed_pass`, `potential_assist`, `turnover`, `ball_start_loc_x`, `ball_start_loc_y`, `ball_end_loc_x`, `ball_end_loc_y`, `action_type`
- Purpose: Tracks passing events with spatial coordinates and outcomes

**Turnovers Table**
- Primary Key: `turnover_id` (Integer)
- Foreign Keys: `player_id` → Players, `game_id` → Games  
- Attributes: `tov_loc_x`, `tov_loc_y`, `action_type`
- Purpose: Records turnover events with location and context

## Normalization Benefits

1. **Eliminates Data Redundancy**: Player and team information is stored once and referenced via foreign keys
2. **Maintains Data Integrity**: Foreign key constraints ensure referential integrity
3. **Supports Complex Queries**: Normalized structure enables efficient aggregation and analysis
4. **Scalable Design**: Easy to add new attributes or entities without affecting existing data

## Spatial Data Considerations

All location-based events (shots, passes, turnovers) store X,Y coordinates as floating-point numbers, enabling spatial analysis and court visualization. The action_type field categorizes events by basketball play type (pickAndRoll, isolation, postUp, offBallScreen) for tactical analysis.

## Query Optimization

The schema supports efficient queries for:
- Player performance aggregation by game, team, or action type
- Spatial analysis of shot/pass/turnover patterns  
- Team statistics and comparative analysis
- Temporal analysis across game dates
