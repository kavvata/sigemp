def login_usecase(username: str, password: str, repo: UserRepository) -> Result:
    user = repo.authenticate(username, password)
    if not user:
        return ResultError("Usuario nao encontrado.")
    return ResultSuccess(user, mensagem="Usuario autenticado com sucesso")
