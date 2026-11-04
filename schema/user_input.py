# Data validation using Pydantic models
from pydantic import BaseModel, Field, ValidationError,computed_field
from typing import  Annotated,Literal
class UserInput(BaseModel):
    # Define schema for user input with validation
    person_age : Annotated[int, Field(gt=0, description="Age must be a positive integer")]
    person_income : Annotated[float, Field(gt=0, description="Income must be a positive number")]
    person_home_ownership :Annotated[Literal['OWN', 'MORTGAGE', 'RENT','OTHER'], 
                                     Field(description="Home ownership status must be one of: " \
                                     "OWN, MORTGAGE, RENT",example="OWN")]
    person_emp_length : Annotated[int, Field(ge=0, le=50, description="Employment length must be between 0 and 50 years")]
    loan_intent : Annotated[Literal['PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE', 'HOMEIMPROVEMENT', 'DEBTCONSOLIDATION'],
                           Field(description="Loan intent must be one of: " \
                           "PERSONAL, EDUCATION, MEDICAL, VENTURE, HOMEIMPROVEMENT, DEBTCONSOLIDATION",example="PERSONAL")]
    loan_grade : Annotated[Literal['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                          Field(description="Loan grade must be one of: A, B, C, D, E, F, G",example="A")]
    loan_amnt : Annotated[float, Field(gt=0, description="Loan amount must be a positive number")]
    loan_int_rate : Annotated[float, Field(gt=0, description="Loan interest rate must be a positive number")]
    cb_person_default_on_file : Annotated[Literal['Y', 'N'], Field(description="Default on file must be either 'Y' or 'N'",example="N")]
    cb_person_cred_hist_length : Annotated[int, Field(ge=0, description="Credit history length must be a non-negative integer")]
    @computed_field
    @property
    def loan_percent_income(self)-> float:
        # Calculate loan percent income based on loan amount and person income
        return (self.loan_amnt / self.person_income)