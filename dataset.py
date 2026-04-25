# dataset.py
# Our golden dataset — the answer key for our eval system

dataset = [

    # TIER 1 — Simple, single-hop questions
    {
        "id": "t1_001",
        "tier": 1,
        "question": "What is your return policy?",
        "expected": "Products can be returned within 30 days of purchase",
        "tags": ["returns", "policy"]
    },
    {
        "id": "t1_002",
        "tier": 1,
        "question": "What payment methods do you accept?",
        "expected": "We accept credit cards, debit cards, and PayPal",
        "tags": ["payment", "policy"]
    },
    {
        "id": "t1_003",
        "tier": 1,
        "question": "How long does shipping take?",
        "expected": "Standard shipping takes 5-7 business days",
        "tags": ["shipping", "policy"]
    },

    # TIER 2 — Medium, requires some reasoning
    {
        "id": "t2_001",
        "tier": 2,
        "question": "I bought a product 25 days ago and it stopped working. Can I return it?",
        "expected": "Yes, you are within the 30 day return window and can return a defective product",
        "tags": ["returns", "defective", "reasoning"]
    },
    {
        "id": "t2_002",
        "tier": 2,
        "question": "I placed an order but never received a confirmation email. What should I do?",
        "expected": "Check spam folder first, then contact support with your order details to verify the order was placed",
        "tags": ["orders", "email", "reasoning"]
    },

    # TIER 3 — Complex, multi-layered questions
    {
        "id": "t3_001",
        "tier": 3,
        "question": "I ordered 3 items on Monday, only 2 arrived, one of the 2 is damaged, and I am traveling next week. What should I do?",
        "expected": "Contact support about the missing item and damaged product. Request an expedited replacement or refund given the travel constraint. Document damage with photos before traveling",
        "tags": ["returns", "shipping", "damaged", "complex", "multi-step"]
    },
    {
        "id": "t3_002",
        "tier": 3,
        "question": "I used a discount code but was charged full price, and now the sale has ended. Am I entitled to the discount?",
        "expected": "Yes, if the discount code was applied at checkout you are entitled to the discounted price. Contact support with your order number and screenshot of the applied code",
        "tags": ["billing", "discount", "complex", "multi-step"]
    }
]