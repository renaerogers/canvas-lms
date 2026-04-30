# Canvas LMS - Codebase Analysis Map

## Repository Overview
- **Total Files Tracked:** 6,161
- **Type:** Ruby on Rails LMS (Learning Management System)
- **License:** GNU Affero General Public License v3

---

## 1. High-Level Architecture

### Pattern: **Monolithic Rails Application**
- **Framework:** Ruby on Rails 7.x
- **Architecture:** MVC with Service Layer
- **Database:** PostgreSQL (sharded for multi-tenant)
- **Web Server:** Puma
- **Frontend:** JavaScript/TypeScript with React components

### Key Architectural Patterns:
| Pattern | Implementation |
|---------|----------------|
| MVC | `app/controllers/`, `app/models/`, `app/views/` |
| Service Layer | `app/services/` |
| API (REST) | `*_api_controller.rb` files |
| API (GraphQL) | `app/graphql/`, `graphql_controller.rb` |
| Middleware | `app/middleware/` |
| Observers | `app/observers/` |

---

## 2. Core Domain Logic

### Primary Directories:
| Directory | Purpose | File Count |
|-----------|---------|-------------|
| `app/controllers/` | HTTP request handlers | 200+ |
| `app/models/` | Data models & business logic | 300+ |
| `app/services/` | Business logic services | 100+ |
| `lib/` | Core library code | ~50 |
| `config/` | Application configuration | ~40 |

### Heavy-Lifting Modules:
- **Course Management:** `app/models/course.rb`, `app/controllers/courses_controller.rb`
- **User/Authentication:** `app/models/user.rb`, `app/models/pseudonym.rb`, `app/controllers/users_controller.rb`
- **Assignments/Submissions:** `app/models/assignment.rb`, `app/models/submission.rb`
- **Grading:** `app/models/score.rb`, `app/models/gradebook_filter.rb`
- **API Layer:** `app/controllers/graphql_controller.rb`, `config/routes.rb`

---

## 3. Entry Points

### Primary Entry Points:
| File | Purpose |
|------|---------|
| `config.ru` | Rack-based server entry point |
| `config/application.rb` | Rails application configuration |
| `config/environment.rb` | Environment initialization |
| `config/boot.rb` | Bootstrapping |
| `config/routes.rb` | Route definitions (800+ routes) |

### HTTP Request Flow:
```
config.ru → config/environment.rb → config/application.rb
    ↓
Rails.application.load_server
    ↓
Routes (config/routes.rb)
    ↓
Controllers (inheriting from ApplicationController)
    ↓
Models/Services
```

### Base Controller:
- `app/controllers/application_controller.rb` - Parent of all controllers
  - Includes: Authentication, API, LocaleSelection, CSRF protection

---

## 4. Index of Importance

### Critical Files (by function):

#### Configuration:
| File | Importance |
|------|-------------|
| `config.ru` | ⭐⭐⭐ Entry point |
| `config/application.rb` | ⭐⭐⭐ Rails config |
| `config/routes.rb` | ⭐⭐⭐ API surface |
| `config/database.yml.example` | ⭐⭐ Database config |
| `Gemfile` | ⭐⭐⭐ Dependencies |

#### Core Application:
| File | Importance |
|------|-------------|
| `app/controllers/application_controller.rb` | ⭐⭐⭐ Base controller |
| `app/models/user.rb` | ⭐⭐⭐ User entity |
| `app/models/course.rb` | ⭐⭐⭐ Course entity |
| `app/models/account.rb` | ⭐⭐⭐ Account entity |

#### Key Controllers:
| File | Purpose |
|------|---------|
| `app/controllers/courses_controller.rb` | Course CRUD |
| `app/controllers/assignments_controller.rb` | Assignment management |
| `app/controllers/submissions_controller.rb` | Submission handling |
| `app/controllers/graphql_controller.rb` | GraphQL API |
| `app/controllers/api/v1/*` | REST API v1 |

#### Key Models:
| File | Purpose |
|------|---------|
| `app/models/user.rb` | User identity & authentication |
| `app/models/course.rb` | Course entity & associations |
| `app/models/enrollment.rb` | Student enrollment tracking |
| `app/models/assignment.rb` | Assignment definitions |
| `app/models/submission.rb` | Student submissions |

#### Services:
| File | Purpose |
|------|---------|
| `app/services/*` | Business logic encapsulation |

---

## 5. Technology Stack

### Backend:
- **Language:** Ruby 3.x
- **Framework:** Rails 7.x
- **Database:** PostgreSQL (with sharding)
- **Cache:** Redis, Memcache
- **Queue:** Delayed::Job

### Frontend:
- **JavaScript:** TypeScript, React
- **Build:** Rspack, Webpack
- **Testing:** Vitest, Jest, RSpec

### Infrastructure:
- **Container:** Docker
- **CI/CD:** Jenkins (Jenkinsfile)
- **Linting:** ESLint, RuboCop, Biome

---

## 6. File Organization Summary

```
canvas-lms/
├── app/                    # Main application code
│   ├── controllers/        # HTTP handlers
│   ├── models/             # Data models
│   ├── services/           # Business logic
│   ├── views/              # ERB templates
│   ├── graphql/            # GraphQL schema
│   └── middleware/         # Rack middleware
├── config/                 # Configuration
│   ├── routes.rb           # Route definitions
│   ├── application.rb      # App config
│   └── environments/       # Env-specific config
├── lib/                    # Core libraries
├── spec/                   # RSpec tests
├── public/                 # Static assets
├── db/                     # Migrations
└── config.ru               # Entry point
```

---

*Generated by Codebase Analyst Agent*
*Analysis based on repo_manifest.json (6,161 files)*