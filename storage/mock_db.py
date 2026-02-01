class MockLeadDB:
    def __init__(self):
        self.leads = []

    def save(self, lead):
        self.leads.append(lead)
        print("💾 Lead saved to mock DB")
        print(lead)
