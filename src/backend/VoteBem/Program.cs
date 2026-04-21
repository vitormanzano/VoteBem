using Microsoft.Extensions.FileProviders;
using VoteBem.Data;
using VoteBem.Repository.Candidaturas;
using VoteBem.Services.Candidatos;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddOpenApi();

builder.Services.AddScoped<ICandidaturaRepository, CandidaturaRepository>();
builder.Services.AddScoped<ICandidatoService, CandidatoService>();

builder.Services.AddDbContext<AppDbContext>(options =>
{
    options.UseNpgsql(connectionString: builder.Configuration.GetConnectionString("PostgresConnection"));
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

app.UseAuthorization();

app.MapControllers();

app.Run();
