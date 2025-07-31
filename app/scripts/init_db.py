from app.database import Base, engine
from app.models import incident, user, department, apparatus, shift, incident_personnel

print("📦 Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
