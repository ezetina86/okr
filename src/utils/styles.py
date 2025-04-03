# src/utils/styles.py

# Company color palette
COLORS = {
    'sea': '#00F6FF',
    'mint': '#00FFF0',
    'lilac': '#B896FF',
    'sky': '#7BA8FF',
    'night': '#060606',
    # Derived colors for different states
    'success': '#00FFF0',  # Using mint for success
    'warning': '#B896FF',  # Using lilac for warning
    'danger': '#FF9696',   # Lighter red that matches the palette
    'background': '#FFFFFF',
    'text': '#060606'      # Using night for text
}

# Common styles for headers
HEADER_STYLE = """
    <style>
        .main-header {
            padding: 1rem;
            background-color: white;
            margin-bottom: 2rem;
        }
        .logo-img {
            max-height: 50px;
            margin-right: 20px;
        }
        .subtitle {
            color: #7BA8FF;
            font-size: 1.5rem;
            margin-bottom: 2rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #00F6FF;
        }
    </style>
"""