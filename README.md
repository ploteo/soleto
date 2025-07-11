# Soleto Economic Experiments

This repository contains experimental economics materials and code for the Summer School & Workshop on Experimetrics & Behavioral Economics, including oTree-based behavioral experiments and course materials.

## 🖼️ Presentation Materials

- **`SLIDES/`** - Contains presentation slides for all modules
  - `PRINTOUT_1.html` - Slides for module 1
  - `PRINTOUT_2.html` - Slides for module 2
  - `PRINTOUT_3.html` - Slides for module 3


## 🔬 oTree Experiments

The `CODE/oTree/` directory contains a complete oTree project with several behavioral economics experiments:

### Available Experiments

1. **MPL (Multiple Price List)** - Risk elicitation à la Holt & Laury
   - Single-player risk preference measurement
   - Uses lottery choices to determine risk attitudes
   - Location: `CODE/oTree/MPL/`

2. **PGG (Public Goods Game)** - Classic public goods experiment
   - 3-player groups, 4 rounds
   - Each player receives 100 currency units endowment
   - 2x multiplier for contributions to public good
   - Location: `CODE/oTree/PGG/`

3. **Group Roles** - Group dynamics and role assignment experiment
   - 4-player groups
   - Location: `CODE/oTree/groups_roles/`

4. **Inputs** - Input validation and form handling demonstration
   - Single participant
   - Various input types (buttons, dropdowns, radio buttons, etc.)
   - Location: `CODE/oTree/inputs/`

## 🔧 Technical Requirements

- **oTree**: >=5.4.0
- **psycopg2**: >=2.8.4 (PostgreSQL adapter)
- **sentry-sdk**: 0.7.9 (Error tracking)

For questions or issues with the experimental code, refer to the [oTree documentation](https://otree.readthedocs.io/) or contact the course instructor.
