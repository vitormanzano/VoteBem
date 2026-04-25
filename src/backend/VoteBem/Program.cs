using Microsoft.Extensions.FileProviders;
using VoteBem.Data;
using VoteBem.Repository.Candidatos;
using VoteBem.Services.Candidatos;
using Microsoft.EntityFrameworkCore;
using VoteBem.Repository.BensCadidato;
using VoteBem.Repository.Candidaturas;
using VoteBem.Services.BensCandidato;
using VoteBem.Services.Candidaturas;

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

builder.Services.AddDbContext<AppDbContext>(options =>
{
    options.UseNpgsql(connectionString: builder.Configuration.GetConnectionString("PostgresConnection"));
});

builder.Services.AddCors(options =>
{
    options.AddPolicy(name: MyAllowSpecificOrigins,
                      policy =>
                      {
                          policy.WithOrigins("*");
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
