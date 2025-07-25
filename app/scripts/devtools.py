import argparse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import user as user_models, department as dept_models
from app.utils import auth as utils

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#----- USER OPERATIONS -----
def create_user(args):
    db = next(get_db())
    hashed_pw = utils.hash_password(args.password)

    new_user = user_models.User(
        dept_id=args.dept_id,
        username=args.username,
        hashed_password=hashed_pw,
        full_name=args.full_name,
        email=args.email,
        role=args.role        
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(f"✅ Created user: {new_user.username} (ID: {new_user.user_id})")

def list_users(args):
    db = next(get_db())
    users = db.query(user_models.User).all()
    for user in users:
        print(f"[{user.user_id}] {user.full_name} ({user.username}) - Role: {user.role} - Dept: {user.dept_id}")

def delete_user(args):
    db = next(get_db())
    user = db.query(user_models.User).filter(user_models.User.user_id == args.user_id).first()
    if not user:
        print("❌ User not found")
        return
    
    confirm = input(f"⚠️ Are you sure you want to delete user '{user.username}' (ID: {user.user_id})? [y/n]: ")
    if confirm.lower() != "y":
        print("❌ Deletion cancelled.")

    db.delete(user)
    db.commit()
    print(f"🗑️ Deleted user ID {args.user_id}")

#----- DEPARTMENT OPERATIONS ----- 
def create_dept(args):
    db = next(get_db())
    dept = dept_models.Department(
        dept_name=args.name,
        location=args.location
    )
    db.add(dept)
    db.commit()
    db.refresh(dept)
    print(f"✅ Created department: {dept.dept_name} (ID: {dept.dept_id})")

def list_depts(args):
    db = next(get_db())
    depts = db.query(dept_models.Department).all()
    for dept in depts:
        print(f"[{dept.dept_id}] {dept.dept_name} - {dept.location}")

def delete_dept(args):
    db = next(get_db())
    dept = db.query(dept_models.Department).filter(dept_models.Department.dept_id == args.dept_id).first()
    if not dept:
        print("❌ Department not found")
        return
    
    confirm = input(f"⚠️ Are you sure you want to delete department '{dept.dept_name}' (ID: {dept.dept_id})? [y/n]: ")
    if confirm.lower() != "y":
        print("❌ Deletion cancelled.")

    db.delete(dept)
    db.commit()
    print(f"🗑️ Deleted department ID {args.dept_id}")

#----- ARGPARSE ROUTER -----
def main():
    parser = argparse.ArgumentParser(description="🛠️ BlackLine DevOps CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    #User commands
    user_create = subparsers.add_parser("add-user")
    user_create.add_argument("--dept-id", type=int, required=True)
    user_create.add_argument("--username", required=True)
    user_create.add_argument("--password", required=True)
    user_create.add_argument("--full-name", required=True)
    user_create.add_argument("--email", required=True)
    user_create.add_argument("--role", default="user")
    user_create.set_defaults(func=create_user)

    user_list = subparsers.add_parser("list-users")
    user_list.set_defaults(func=list_users)

    user_delete = subparsers.add_parser("delete-user")
    user_delete.add_argument("--user-id", type=int, required=True)
    user_delete.set_defaults(func=delete_user)

    #Department commands
    dept_create = subparsers.add_parser("add-dept")
    dept_create.add_argument("--name", required=True)
    dept_create.add_argument("--location", required=True)
    dept_create.set_defaults(func=create_dept)

    dept_list = subparsers.add_parser("list-depts")
    dept_list.set_defaults(func=list_depts)

    dept_delete = subparsers.add_parser("delete-dept")
    dept_delete.add_argument("--dept-id", type=int, required=True)
    dept_delete.set_defaults(func=delete_dept)

    #Parse & dispatch
    args= parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

                             