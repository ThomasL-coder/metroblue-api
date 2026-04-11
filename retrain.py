from Project.lead_scoring.train import main as train_lead_model


if __name__ == "__main__":
    print("Retraining lead scoring model...")
    train_lead_model()
    print("Retraining completed")
