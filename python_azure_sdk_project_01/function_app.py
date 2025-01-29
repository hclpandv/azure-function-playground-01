import azure.functions as func
import logging
import azure.identity
import azure.keyvault.secrets

app = func.FunctionApp()

@app.timer_trigger(schedule="0 */1 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def get_akv_secret(myTimer: func.TimerRequest) -> None:
    
    if myTimer.past_due:
        logging.info('The timer is past due!')
    
    VAULT_URL = "https://vikivault02.vault.azure.net/"
    SECRET_NAME = "vikisecret"

    logging.info(f"Retrieving secret: {SECRET_NAME} from {VAULT_URL}")

    DB_PASSWORD = azure.keyvault.secrets.SecretClient(
        vault_url=VAULT_URL,
        credential=azure.identity.ManagedIdentityCredential()
    ).get_secret(SECRET_NAME).value
    
    logging.info(f"Successfully retrieved secret: {SECRET_NAME} - Value: {DB_PASSWORD}")
    logging.info('Python timer trigger function executed.')

