using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.FileProviders;
using VoteBem.Data;
using VoteBem.Repository.BensCadidato;
using VoteBem.Repository.Candidatos;
using VoteBem.Repository.Candidaturas;
using VoteBem.Repository.NotasFiscais;
using VoteBem.Repository.RedesSociais;
using VoteBem.Repository.ResumosProposta;
using VoteBem.Repository.SituacaoJuridica;
using VoteBem.Services.BensCandidato;
using VoteBem.Services.Candidatos;
using VoteBem.Services.Candidaturas;
using VoteBem.Services.IA;
using VoteBem.Services.NotasFiscais;
using VoteBem.Services.RedesSociais;
using VoteBem.Services.SituacaoJuridica;

var MyAllowSpecificOrigins = "_myAllowSpecificOrigins";

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddOpenApi();

builder.Services.AddScoped<ICandidatoRepository, CandidatoRepository>();
builder.Services.AddScoped<ICandidatoService, CandidatoService>();
builder.Services.AddScoped<IBemCandidatoRepository, BemCandidatoRepository>();
builder.Services.AddScoped<IBemCandidatoService, BemCandidatoService>();
builder.Services.AddScoped<ICandidaturaRepository, CandidaturaRepository>();
builder.Services.AddScoped<ICandidaturaService, CandidaturaService>();
builder.Services.AddScoped<ISituacaoJuridicaRepository, SituacaoJuridicaRepository>();
builder.Services.AddScoped<ISituacaoJuridicaService, SituacaoJuridicaService>();
builder.Services.AddScoped<INotaFiscalRepository, NotaFiscalRepository>();
builder.Services.AddScoped<INotaFiscalService, NotaFiscalService>();
builder.Services.AddScoped<IRedeSocialRepository, RedeSocialRepository>();
builder.Services.AddScoped<IRedeSocialService, RedeSocialService>();
builder.Services.AddScoped<IResumoPropostaRepository, ResumoPropostaRepository>();

builder.Services.AddHttpClient<IAiService, AiService>(client =>
{
    var baseUrl = builder.Configuration["Ai:BaseUrl"] ?? "http://127.0.0.1:8001";
    client.BaseAddress = new Uri(baseUrl.TrimEnd('/') + "/");
    client.Timeout = TimeSpan.FromSeconds(60);
});

builder.Services.AddDbContext<AppDbContext>(options =>
{
    options.UseNpgsql(connectionString: builder.Configuration.GetConnectionString("PostgresConnection"));
});

builder.Services.AddCors(options =>
{
    options.AddPolicy(name: MyAllowSpecificOrigins,
                      policy =>
                      {
                          policy.AllowAnyOrigin()
                                .AllowAnyMethod()
                                .AllowAnyHeader();
                      });
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();

// Serve etl/data/storage/ under /storage
var storagePath = Path.GetFullPath(
    Path.Combine(builder.Environment.ContentRootPath, "..", "..", "..", "etl", "data", "storage")
);
if (Directory.Exists(storagePath))
{
    app.UseStaticFiles(new StaticFileOptions
    {
        FileProvider = new PhysicalFileProvider(storagePath),
        RequestPath = "/storage"
    });
}

app.UseCors(MyAllowSpecificOrigins);

app.UseAuthorization();

app.MapControllers();

app.Run();
