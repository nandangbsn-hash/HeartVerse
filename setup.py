"""
HeartVerse Project Initialization Script

This script:
1. Validates project structure
2. Creates necessary directories
3. Installs Python dependencies
4. Generates synthetic data
5. Trains ML models
6. Prepares backend for deployment

Usage:
    python setup.py
"""

import os
import sys
import subprocess
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HeartVerseSetup:
    """Setup and initialization for HeartVerse project."""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.success = True
    
    def check_python_version(self):
        """Verify Python version >= 3.9."""
        logger.info("[1/7] Checking Python version...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 9):
            logger.error(f"Python 3.9+ required, got {version.major}.{version.minor}")
            self.success = False
            return
        
        logger.info(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    
    def check_directories(self):
        """Verify project structure."""
        logger.info("[2/7] Checking project structure...")
        
        required_dirs = [
            'ml', 'ml/models', 'ml/evaluation_results',
            'backend', 'datasets', 'docs'
        ]
        
        for dir_name in required_dirs:
            dir_path = self.root_dir / dir_name
            if not dir_path.exists():
                logger.warning(f"Creating missing directory: {dir_name}")
                dir_path.mkdir(parents=True, exist_ok=True)
        
        logger.info("✓ All directories present")
    
    def install_dependencies(self):
        """Install Python dependencies."""
        logger.info("[3/7] Installing Python dependencies...")
        
        try:
            req_file = self.root_dir / 'requirements.txt'
            if not req_file.exists():
                logger.error(f"requirements.txt not found at {req_file}")
                self.success = False
                return
            
            logger.info("Running: pip install -r requirements.txt")
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-r', str(req_file)],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.warning("Some packages may not have installed correctly")
                logger.debug(result.stderr)
            else:
                logger.info("✓ Dependencies installed")
        
        except Exception as e:
            logger.error(f"Failed to install dependencies: {e}")
            self.success = False
    
    def generate_data(self):
        """Generate synthetic cardiovascular dataset."""
        logger.info("[4/7] Preparing datasets...")
        
        try:
            sys.path.insert(0, str(self.root_dir))
            
            from datasets.prepare_datasets import prepare_all_datasets
            prepare_all_datasets()
            
            logger.info("✓ Datasets ready")
        
        except Exception as e:
            logger.error(f"Failed to prepare datasets: {e}")
            self.success = False
    
    def train_models(self):
        """Train ML models."""
        logger.info("[5/7] Training ML models...")
        
        try:
            sys.path.insert(0, str(self.root_dir))
            
            from run_ml_pipeline import main as run_pipeline
            run_pipeline()
            
            logger.info("✓ Models trained")
        
        except Exception as e:
            logger.error(f"Failed to train models: {e}")
            logger.warning("You can train models later with: python run_ml_pipeline.py")
    
    def install_backend_deps(self):
        """Install backend-specific dependencies."""
        logger.info("[6/7] Installing backend dependencies...")
        
        try:
            backend_req = self.root_dir / 'backend' / 'requirements.txt'
            if not backend_req.exists():
                logger.warning(f"Backend requirements.txt not found")
                return
            
            logger.info("Running: pip install -r backend/requirements.txt")
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-r', str(backend_req)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("✓ Backend dependencies installed")
            else:
                logger.warning("Some backend packages may not have installed")
        
        except Exception as e:
            logger.warning(f"Backend setup optional: {e}")
    
    def generate_startup_script(self):
        """Generate startup scripts."""
        logger.info("[7/7] Generating startup scripts...")
        
        try:
            # Windows batch file
            batch_content = """@echo off
echo Starting HeartVerse...
echo.
echo Backend: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
python -m venv venv 2>nul
call venv\\Scripts\\activate.bat
cd backend
python app.py
"""
            
            with open(self.root_dir / 'start_backend.bat', 'w') as f:
                f.write(batch_content)
            
            # Bash script
            bash_content = """#!/bin/bash
echo "Starting HeartVerse..."
echo ""
echo "Backend: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
python -m venv venv 2>/dev/null
source venv/bin/activate
cd backend
python app.py
"""
            
            with open(self.root_dir / 'start_backend.sh', 'w') as f:
                f.write(bash_content)
            
            # Make bash script executable
            os.chmod(self.root_dir / 'start_backend.sh', 0o755)
            
            logger.info("✓ Startup scripts created")
        
        except Exception as e:
            logger.warning(f"Could not create startup scripts: {e}")
    
    def run_setup(self):
        """Run complete setup."""
        logger.info("="*70)
        logger.info("HEARTVERSE PROJECT INITIALIZATION")
        logger.info("="*70 + "\n")
        
        self.check_python_version()
        self.check_directories()
        self.install_dependencies()
        self.generate_data()
        self.train_models()
        self.install_backend_deps()
        self.generate_startup_script()
        
        logger.info("\n" + "="*70)
        if self.success:
            logger.info("✓ SETUP COMPLETE!")
        else:
            logger.warning("⚠ Setup completed with some warnings")
        logger.info("="*70)
        
        logger.info("\nNext steps:")
        logger.info("1. Review model evaluation in ml/evaluation_results/")
        logger.info("2. Start backend: python backend/app.py")
        logger.info("3. Test API at: http://localhost:8000/docs")
        logger.info("4. Build frontend when ready")
        logger.info("\nQuick Start Guide: See QUICKSTART.md")


if __name__ == "__main__":
    setup = HeartVerseSetup()
    setup.run_setup()
